import argparse
from FruitsChecker import FruitsChecker

FRUITS_TYPE = "apple" # リンゴを対象にする

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--in_image",  required=True)
    parser.add_argument("--out_image")
    parser.add_argument("--out_csv")
    args = parser.parse_args()

    # FruitsCheckerをインスタンス化して処理を実行する
    checker = FruitsChecker(args.in_image, args.out_image, args.out_csv, FRUITS_TYPE)
    checker.process()

if __name__ == "__main__":
    main()