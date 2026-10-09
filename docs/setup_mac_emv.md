Setup Software Development Environment on macOS
This guide provides step-by-step instructions for configuring a complete development environment for Java, Python, and TypeScript on macOS, including verification steps after each component installation.

1. Package Manager (Homebrew)
Install Homebrew, the standard package manager for macOS:

Bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Configure PATH (Apple Silicon)
On Apple Silicon Macs (M1/M2/M3/M4), Homebrew installs to /opt/homebrew. Add it to your shell profile if it is not already in your PATH:

Bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
eval "$(/opt/homebrew/bin/brew shellenv)"
Verification
Verify Homebrew is installed and functioning properly:

Bash
brew --version
brew doctor



2. Version Control (Git)
Install Git:

Bash
brew install git
Configure your global Git identity:

Bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
Verification
Verify Git installation and current global configuration:

Bash
git --version
git config --list --global



3. Programming Languages & Runtimes
3.1 Java (JDK)
Install OpenJDK via Homebrew:

Bash
brew install openjdk
Symlink OpenJDK so the system Java wrappers can find it:

Bash
sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
Configure JAVA_HOME and update PATH in ~/.zshrc:

Bash
echo 'export JAVA_HOME=$(/usr/libexec/java_home)' >> ~/.zshrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
Verification
Verify Java compiler and runtime installation along with JAVA_HOME configuration:

Bash
java -version
javac -version
echo $JAVA_HOME




3.2 Python
Install Python 3:

Bash
brew install python
Add Homebrew's Python binary directory to your PATH in ~/.zshrc:

Bash
echo 'export PATH="$(brew --prefix)/opt/python/libexec/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
Verification
Verify Python 3 and pip installation:

Bash
python3 --version
pip3 --version
which python3





3.3 Node.js & TypeScript
Install Node.js (includes npm):

Bash
brew install node
Install TypeScript globally:

Bash
npm install -g typescript
Verification
Verify Node.js, npm, and TypeScript installations:

Bash
node -v
npm -v
tsc -v
4. Integrated Development Environments (IDEs)
4.1 Visual Studio Code
Install VS Code via Homebrew Cask:

Bash
brew install --cask visual-studio-code
Recommended Extensions
Install common language extensions via the terminal:

Bash
# Java Extension Pack
code --install-extension vscjava.vscode-java-pack

# Python Extension
code --install-extension ms-python.python

# ESLint for TypeScript/JavaScript
code --install-extension dbaeumer.vscode-eslint
Verification
Verify VS Code CLI tool installation:

Bash
code --version
4.2 JetBrains IDEs (Optional)
Install dedicated IDEs for Java and Python development:

Bash
# IntelliJ IDEA (Java)
brew install --cask intellij-idea

# PyCharm (Python)
brew install --cask pycharm
5. Environment Smoke Test
Create and execute a quick test script for each language environment to confirm compilation and execution works as expected.

5.1 Java Test
Create a file named HelloWorld.java:

Java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Java environment is working!");
    }
}
Compile and run:

Bash
javac HelloWorld.java
java HelloWorld
5.2 Python Test
Run a quick inline Python script:

Bash
python3 -c 'print("Python environment is working!")'
5.3 TypeScript Test
Create a file named test.ts:

TypeScript
const message: string = "TypeScript environment is working!";
console.log(message);
Compile to JavaScript and execute with Node.js:

Bash
tsc test.ts
node test.js

To verify: 
weipeng@Weipengs-MacBook-Pro ~ % 
weipeng@Weipengs-MacBook-Pro ~ % node -v
v24.21.0
weipeng@Weipengs-MacBook-Pro ~ % npm -v
11.19.0
weipeng@Weipengs-MacBook-Pro ~ % tsc -v
Version 7.0.2
weipeng@Weipengs-MacBook-Pro ~ % java -version
java version "27" 2026-09-15
Java(TM) SE Runtime Environment (build 27+35-2325)
Java HotSpot(TM) 64-Bit Server VM (build 27+35-2325, mixed mode, sharing)
weipeng@Weipengs-MacBook-Pro ~ % brew --version
Homebrew 7.0.9
weipeng@Weipengs-MacBook-Pro ~ % git --version
git version 2.56.0
weipeng@Weipengs-MacBook-Pro ~ % python3 --version
Python 3.14.8
weipeng@Weipengs-MacBook-Pro ~ % pip3 --version
pip 26.2.1 from /Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/pip (python 3.14)
weipeng@Weipengs-MacBook-Pro ~ % npx playwright --version
Version 1.64.0
weipeng@Weipengs-MacBook-Pro ~ % 

