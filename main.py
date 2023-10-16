import pickle, argparse, json, os
from Dict import Dict
from icecream import ic
from tqdm import tqdm

def read_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-data_dir', type=str, default='/home/manh/Documents/Data/splited-tan-dataset')
    parser.add_argument('-project', type=str, default='bootstrap')
    parser.add_argument('-detail', type=str, default='begin_to_2021')

    return parser

def filter_duplicate(my_list: list):
    unique_dict = {}
    for dictionary in tqdm(my_list):
        key = json.dumps(dictionary, sort_keys=True)
        unique_dict[key] = dictionary

    # Get the unique elements from the dictionary
    unique_elements = list(unique_dict.values())

    return unique_elements

def split_sentence(sentence):
    sentence = sentence.replace('.', ' . ').replace('_', ' ').replace('@', ' @ ')\
        .replace('-', ' - ').replace('~', ' ~ ').replace('%', ' % ').replace('^', ' ^ ')\
        .replace('&', ' & ').replace('*', ' * ').replace('(', ' ( ').replace(')', ' ) ')\
        .replace('+', ' + ').replace('=', ' = ').replace('{', ' { ').replace('}', ' } ')\
        .replace('|', ' | ').replace('\\', ' \ ').replace('[', ' [ ').replace(']', ' ] ')\
        .replace(':', ' : ').replace(';', ' ; ').replace(',', ' , ').replace('<', ' < ')\
        .replace('>', ' > ').replace('?', ' ? ').replace('/', ' / ')
    sentence = ' '.join(sentence.split())
    return sentence

def main():
    params = read_args().parse_args()
    ic(params.data_dir)
    ic(params.project)
    ic(params.detail)

    if os.path.exists(f"{params.data_dir}/{params.project}/commits/{params.project}_{params.detail}_dict.pkl"):
        ic("Already preprocessed")
        return

    data = pickle.load(open(f'{params.data_dir}/{params.project}/{params.project}_{params.detail}.pkl', 'rb'))
    ic(len(data))

    msg_dict = Dict(lower=True)
    code_dict = Dict(lower=True)

    for commit in tqdm(data):
        filterd_commit = filter_duplicate(commit['main_language_file_changes'])
        commit['main_language_file_changes'] = filterd_commit

    ids = []
    messages = []
    cc2vec_commits = []
    deepjit_commits = []
    labels = []

    for commit in tqdm(data):
        message = commit['commit_message'].strip()
        message = split_sentence(message)
        message = ' '.join(message.split(' ')).lower()

        for word in message.split():
            msg_dict.add(word)

        cc2vec_commit = []
        deepjit_commit = []
        for file in commit['main_language_file_changes']:
            list_of_added_code = []
            list_of_removed_code = []
            for hunk in file['code_changes']:
                added_code = hunk['added_code']
                removed_code = hunk['removed_code']

                added_code = added_code.strip()
                removed_code = removed_code.strip()

                added_code = ' '.join(split_sentence(added_code).split())
                removed_code = ' '.join(split_sentence
                (removed_code).split())

                added_code = ' '.join(added_code.split(' '))
                removed_code = ' '.join(removed_code.split(' '))

                list_of_added_code.append(added_code)
                list_of_removed_code.append(removed_code)
                deepjit_commit.append(added_code)
                deepjit_commit.append(removed_code)

                for word in added_code.split():
                    code_dict.add(word)
                for word in removed_code.split():
                    code_dict.add(word)
            
            cc2vec_commit.append({
                'added_code': list_of_added_code,
                'removed_code': list_of_removed_code
            })

        ids.append(commit['commit_hash'])
        messages.append(message)
        cc2vec_commits.append(cc2vec_commit)
        deepjit_commits.append(deepjit_commit)
        labels.append(commit['bug_inducing'])
            
    msg_dict = msg_dict.prune(100000)
    code_dict = code_dict.prune(100000)
    project_dict = [msg_dict.get_dict(), code_dict.get_dict()]

    cc2vec_preprocessed_train = [ids, messages, cc2vec_commits, labels]
    deepjit_preprocessed_train = [ids, messages, deepjit_commits, labels]

    if not os.path.exists(f"{params.data_dir}/{params.project}/commits"):
        os.makedirs(f"{params.data_dir}/{params.project}/commits")

    pickle.dump(project_dict, open(f"{params.data_dir}/{params.project}/commits/{params.project}_{params.detail}_dict.pkl", 'wb'))
    pickle.dump(cc2vec_preprocessed_train, open(f"{params.data_dir}/{params.project}/commits/{params.project}_{params.detail}.pkl", 'wb'))
    pickle.dump(deepjit_preprocessed_train, open(f"{params.data_dir}/{params.project}/commits/{params.project}_{params.detail}_dextend.pkl", 'wb'))

if __name__ == "__main__":
    main()