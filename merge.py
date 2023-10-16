import pickle, argparse, os
from icecream import ic
from tqdm import tqdm

def read_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-data_dir', type=str, default='/home/manh/Documents/Data/splited-tan-dataset')
    parser.add_argument('-project', type=str, default='bootstrap')
    parser.add_argument('-details', type=str, default=[], nargs='+')

    return parser

def main():
    params = read_args().parse_args()

    data_dir = params.data_dir
    ic(data_dir)
    project = params.project
    ic(project)
    details = params.details
    ic(details)

    concated_data = []

    for detail in details:
        file_path = f"{data_dir}/{project}/{project}_{detail}.pkl"

        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                ic(type(data))
                ic(len(data))

                concated_data += data
                
                # Process the project_data as needed
                ic(f"Loaded data for project: {file_path}")
        except FileNotFoundError:
            ic(f"File not found for project: {file_path}")

    ic(len(concated_data))

    ic(pickle.dump(concated_data, open(f"{data_dir}/{project}/{project}_{details[0]}_{details[-1]}.pkl", 'wb')))

if __name__ == "__main__":
    main()