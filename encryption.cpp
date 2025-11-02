#include <iostream>
#include <sstream>
#include <vector>
#include <iomanip>
#include <fstream>
#include <random>
#include <chrono>
#include "AES.h"

using namespace std;

// Convert string to bytes
vector<uint8_t> stringToBytes(const string& str) {
    return vector<uint8_t>(str.begin(), str.end());
}

// Convert bytes to hex string
string bytesToHex(const vector<uint8_t>& data) {
    stringstream ss;
    ss << hex << setfill('0');
    for (uint8_t byte : data) {
        ss << setw(2) << (int)byte;
    }
    return ss.str();
}

// Generate random 16-byte AES key
vector<uint8_t> genRandomKey() {
    vector<uint8_t> key(16);
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    default_random_engine rng(seed);
    uniform_int_distribution<int> dist(0, 255);
    for (int i = 0; i < 16; i++) key[i] = dist(rng);
    return key;
}

int main() {
    string plaintext=" ";
    cout << "Enter plaintext (max 16 chars): ";
    fstream fil("database.txt",ios::out);
    getline(cin, plaintext);

    // Pad plaintext to 16 bytes
    while (plaintext.size() < 16) plaintext.push_back('\0');

    vector<uint8_t> plainBytes = stringToBytes(plaintext);
    vector<uint8_t> key = genRandomKey();
    uint8_t cipher[16];
    AES128_EncryptBlock(plainBytes.data(), key.data(), cipher);

    vector<uint8_t> cipherVec(cipher, cipher + 16);

    cout << "Ciphertext (hex): " << bytesToHex(cipherVec) << endl;
    fil<< bytesToHex(cipherVec) << endl;
    cout << "Key (hex): " << bytesToHex(key) << endl;
    fil<< bytesToHex(key) << endl;
    fil.close();
    return 0;
}

