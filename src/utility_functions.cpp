/**
 * @file: utility_functions.cpp
 * @author: kaythegemini
 * 
 * Implementation of the utility functions
 */
#include "utility_functions.h"
#include <filesystem>
namespace fs = std::filesystem;

Config::Config(const std::string& directory, const std::string& filename)
{
  // Ensure the directory exists
    if (!fs::exists(directory))
    {
        if (!fs::create_directories(directory))
        {
            std::cerr << "Failed to create directory: " << directory << std::endl;
            return;
        }
    }

    // Set the file path
    filepath = directory + "/" + filename;

    // Load existing JSON data if the file exists
    std::ifstream file(filepath);
    if (file.is_open())
    {
        file >> jsonData;
        file.close();
    }
    else
    {
        // Initialize jsonData to an empty object if file its not open or empty
        jsonData = nlohmann::json::object();
    }

}

std::string Config::read(const std::string& key, const std::string& defaultValue) {
    if (jsonData.is_null())
    {
        return defaultValue;
    }
    return jsonData.value(key, defaultValue);
}

void Config::write(const std::string& key, const std::string& value) {
    jsonData[key] = value;
    std::ofstream file(filepath);
    if (file.is_open()) {
        file << jsonData.dump(4);
        file.close();
    }
}

bool isInteger(const std::string& string) {
    return !string.empty() && std::all_of(string.begin(), string.end(), ::isdigit);
}

int toInteger(const std::string& string) {
    int out = -1;
    if (isInteger(string)) {
        out = std::stoi(string);
    }
    return out;
}

bool fileExists(const std::string& filename) {
    std::ifstream file(filename);
    return file.good();
}

void askRunScript(const std::string& scriptPath, const std::string& jsonFilePath) {
    // Check if the file already exists, automatically run script if it doesn't
    if (!fileExists(jsonFilePath)) {
        std::cout << jsonFilePath << " does not exist. Running script automatically." << std::endl;
        std::string runCommand = "python -u " + scriptPath;
        int result = system(runCommand.c_str()); // run the script

        if (result == 0) {
            std::cout << "Script executed successfully." << std::endl;
        } else {
            std::cerr << "Failed to execute script." << std::endl;
        }
        return;
    }
    

    // If file already exists, prompt to ask to update
    char userInput;
    while (true) {
        std::cout << "Would you like to run the fetch airports script for possible updates? (y/n): \n> ";
        std::cin >> userInput;


        if (userInput == 'y' || userInput == 'Y') {
            std::string runCommand = "python -u " + scriptPath;
            std::cout << runCommand << std::endl;
            int result = system(runCommand.c_str());

            if (result == 0) {
                std::cout << "script executed successfully." << std::endl;
            } else {
                std::cerr << "Failed to execute script." << std::endl;
            }
            break; // break from the loop after running script
        } else if (userInput == 'n' || userInput == 'N') {
            std::cout << "Proceeding with existing file..." << std::endl;
            break; // break from the loop
        } else {
            std::cout << "Invalid input. Please enter 'y' or 'n'." << std::endl;
        }
    }
    
}

bool prompt(const std::string& question) {
    char userInput;
    while(true) {
        std::cout << question << " (y/n): ";
        std::cin >> userInput;

        if (userInput == 'y' || userInput == 'Y') {
            return true;
        } else if (userInput == 'n' || userInput == 'N') {
            return false;
        } else {
            std::cout << "Invalid input. Please enter 'y' or 'n'." << std::endl;
        }
    }
}

std::string toUpperCase(std::string str) {
    std::string out;
    for (auto& c : str) out += toupper(c);
    return out;
}

int promptRange() {
    std::string input; // Will hold the string input OR the value from read()
    int out = 0; // Will carry the integer value of input and be returned

    // Open the config file if it exists or create it if it doesn't
    Config config("Settings", "config.json");
    // Checking if user.range already exists from before and returning it if it does
    out = toInteger(config.read("user.range", "0"));
    
    if (out > 0) {
        // std::cout << "Using saved range: " << out << "nm" << std::endl;
        return out;
    }

    // Allow user to input their range.
    std::cout << "It seems this is your first time running the program" << std::endl;
    std::cout << "Please enter the range of your aircraft (in nautical miles): \n> ";
    std::cin >> input;

    config.write("user.range", input);

    // Ensure input is an integer
    while (!isInteger(input)) {
        std::cin.clear();
        std::cin.ignore((std::numeric_limits<std::streamsize>::max)(), '\n'); // skip invalid input
        // system("cls");
        std::cout << "\033[31m" << "Not a valid input. Please enter a Number: \n> " << "\033[0m";
        std::cin >> input;
    }

    std::cout << "\nRange saved to config.json." << std::endl;
    return toInteger(input);
}
