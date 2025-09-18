#codigo para a instalação do playwright

from playwright.sync_api import sync_playwright

def install_browsers():
    from playwright.__main__ import main
    import sys
    sys.argv = ["playwright", "install"]
    main()

if __name__ == "__main__":
    install_browsers()
