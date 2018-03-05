# BORD
BORD, which stands for **B**rew **O**ffline **R**ecursive **D**ownloader, is a tool that can be used to move homebrew packages to an offline environment.

# Releases
The only version of BORD so far is 0.1. It is incomplete and not yet stable. Please report issues at [https://github.com/barnabycolby/BORD/issues](https://github.com/barnabycolby/BORD/issues).

# How to use BORD
To use BORD, simply supply the name of the package you wish to retrieve. BORD will figure out the list of dependencies, and then retrieve them as bottles. These bottles should be transferred to the brew cache, which can be found by running `brew --cache`. This is normally `~/Library/Caches/Homebrew`.

For example, to install the *tmux* package on an offline system, the following commands should be used.
```sh
# Online machine
python3 bord.py tmux
cp -r tmux <usb stick>

# Offline machine
cp -r <usb stick>/tmux/* $(brew --cache)
brew install tmux
```
