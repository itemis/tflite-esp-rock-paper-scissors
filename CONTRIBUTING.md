# Contribution Guidelines

Pull requests are welcome.
We don't have a specific template for PRs.
Please follow style guides for Python and C++.

## Python

For Python style, we follow [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/).

## C++/Arduino

For C++ we follow the [Google style guide](https://google.github.io/styleguide/cppguide.html).
We encourage you to run your code against clang-tidy and clang-format.
Once clang-tidy and clang-format are installed, you can do so as follows.

    cd src/tinyml_deployment
    get_idf
    idf.py build
    chmod +x clean_compile_commands.sh
    ./clean_compile_commands.sh
    clang-tidy main/src/*.cpp -p build/
    clang-format main/src/*.cpp -i

## Architecture

Please follow the structure laid out in [ARCHITECTURE.md](ARCHITECTURE.md).