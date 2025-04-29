import argparse


def main():
    parser = argparse.ArgumentParser(description='Sample script')
    parser.add_argument('--name', type=str, help='Name of the person')
    parser.add_argument('--age', type=int, help='Age of the person')
    args = parser.parse_args()
    print(f"Name: {args.name}")
    print(f"Age: {args.age}")
    return 0

if __name__ == '__main__':
    main()

