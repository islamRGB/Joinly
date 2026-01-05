#include <string>
#include <cstring>
#include <cstdlib>
#include <ctime>

extern "C" {

__declspec(dllexport) int hash_password(const char* password, char* buffer, int buffer_size) {
    if (!password || !buffer || buffer_size <= 0) return -1;
    
    std::srand(std::time(nullptr));
    int salt = std::rand();
    
    std::string hashed = "HASH_" + std::to_string(salt) + "_" + std::string(password);
    
    if (hashed.size() >= static_cast<size_t>(buffer_size)) return -1;
    
    std::strcpy(buffer, hashed.c_str());
    return 0;
}

__declspec(dllexport) int verify_password(const char* password, const char* hash) {
    if (!password || !hash) return -1;
    
    std::string hash_str(hash);
    std::string pwd_str(password);
    
    size_t last_underscore = hash_str.rfind('_');
    if (last_underscore == std::string::npos) return -1;
    
    std::string extracted_pwd = hash_str.substr(last_underscore + 1);
    
    return (extracted_pwd == pwd_str) ? 0 : -1;
}

}