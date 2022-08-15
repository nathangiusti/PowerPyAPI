def generate_dev_test_names(names: [str], include_dev: bool, include_test: bool) -> [str]:
    name_len = len(names)
    if include_dev:
        for i in range(0, name_len):
            names.append(names[i] + " [Dev]")
    if include_test:
        for i in range(0, name_len):
            names.append(names[i] + " [Test]")
    return names
