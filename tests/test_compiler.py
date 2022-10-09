def test_compile(project, compiler):
    paths = [
        project.contracts_folder / "MultipleContracts.sol",
        project.contracts_folder / "Proxy.sol",
    ]

    contracts = compiler.compile(paths)
    assert len(contracts) == 4
    assert set(result.name for result in contracts) == {
        "Contract1",
        "Contract2",
        "IDummyInterface",
        "Proxy",
    }
    assert set(result.source_id for result in contracts) == {"MultipleContracts.sol", "Proxy.sol"}
    assert project.Contract1
    assert project.Contract2
    assert project.Proxy
    assert project.IDummyInterface
