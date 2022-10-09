import ape
import pytest


@pytest.mark.skip(reason="integration test on goerli so needs to spend gas there")
def test_integration(project, provider_context, compiler):
    account = ape.accounts.load("goerli")
    print("account is", account)
    compiler.compile([project.contracts_folder / "TestDapp.sol"])
    with provider_context:
        contract = project.TestDapp.at("0x75169c03608F284dD78E6a0cfc71f4bA06BC5DE2")
        print("value before", contract.userNumbers(account.address))
        result = contract.setNumber(69, sender=account, type=0)
        print("tx result", result)
        print("value after", contract.userNumbers(account.address))
