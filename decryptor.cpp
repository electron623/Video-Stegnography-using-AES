#include <iostream>
#include <sstream>
#include <vector>
#include <iomanip>
#include <fstream>
#include <algorithm>
#include <cctype>
#include "AES.h"

using namespace std;

// Convert hex string to bytes
vector<uint8_t> hexToBytes(const string& hex) {
    vector<uint8_t> bytes;
    for (size_t i = 0; i < hex.length(); i += 2) {
        uint8_t byte = stoi(hex.substr(i, 2), nullptr, 16);
        bytes.push_back(byte);
    }
    return bytes;
}

// Convert bytes to printable string
string bytesToString(const vector<uint8_t>& data) {
    string s;
    for (uint8_t b : data) {
        s += static_cast<char>(b);
    }
    return s;
}

int main() {
    fstream fil("database.txt",ios::in);
    string line;
    string cipherHex, keyHex;
    int lineno=0;
    while(getline(fil,line)){
        lineno++;
        if(lineno==1){
            cipherHex=line;
        }
        else if(lineno==2){
            keyHex=line;
        }
        
    }
    // cout << "Enter ciphertext (32 hex chars): ";
    // cin >> cipherHex;
    auto trim = [](std::string &s) {
    s.erase(remove_if(s.begin(), s.end(), [](unsigned char c){ return std::isspace(c); }), s.end());
    };
    trim(cipherHex);
    trim(keyHex);
    cout<<cipherHex<<"\n";
    cout<<keyHex<<"\n";
    if (cipherHex.length() != 32) {
        cerr << "Error: Ciphertext must be 16 bytes (32 hex chars)." << endl;
        return 1;
    }

    // cout << "Enter key (32 hex chars): ";
    // cin >> keyHex;
    if (keyHex.length() != 32) {
        cerr << "Error: Key must be 16 bytes (32 hex chars)." << endl;
        return 1;
    }

    vector<uint8_t> cipherBytes = hexToBytes(cipherHex);
    vector<uint8_t> keyBytes = hexToBytes(keyHex);

    uint8_t plain[16];
    AES128_DecryptBlock(cipherBytes.data(), keyBytes.data(), plain);

    cout << "Decrypted plaintext (raw bytes): ";
    for (int i = 0; i < 16; i++) {
        cout << hex << setw(2) << setfill('0') << (int)plain[i] << " ";
    }
    cout << endl;

    cout << "Printable view: " << bytesToString(vector<uint8_t>(plain, plain + 16)) << endl;

    return 0;
}

