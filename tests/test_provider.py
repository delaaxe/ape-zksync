def test_provider(provider_context):
    with provider_context as provider:
        address = "0x574B685fDE8464ceDd7CE57d254881B11DaF0814"
        balance = provider.get_balance(address)
        print("my balance", balance / 1e18)
        assert balance > 0
