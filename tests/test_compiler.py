def test_compile(project, compiler):
    paths = [
        project.contracts_folder / "TestDapp.sol",
        project.contracts_folder / "Proxy.sol",
    ]

    contracts = compiler.compile(paths)
    assert len(contracts) == 4
    assert set(result.name for result in contracts) == {
        "TestDapp",
        "TestDapp2",
        "IDummyInterface",
        "Proxy",
    }
    assert set(result.source_id for result in contracts) == {"TestDapp.sol", "Proxy.sol"}
    assert project.TestDapp
    assert project.TestDapp2
    assert project.Proxy
    assert project.IDummyInterface
