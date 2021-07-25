import eth_account


def main():
    a = eth_account.Account()

    a.enable_unaudited_hdwallet_features()
    in_ = input("Please paste your 24 key backup phrase!\n")
    local_account = a.from_mnemonic(in_)
    with open("ethereum_private_key.txt", "w") as f:
        f.write(str(local_account.privateKey.hex()))
    print(f"Written key to file.")

    
if __name__ == "__main__":
    main()