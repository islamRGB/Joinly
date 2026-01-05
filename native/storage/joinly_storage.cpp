#include <map>
#include <string>
#include <cstring>

static std::map<std::string, std::string> storage;

extern "C" {

__declspec(dllexport) int native_set(const char* key, const char* value) {
    if (!key || !value) return -1;
    storage[std::string(key)] = std::string(value);
    return 0;
}

__declspec(dllexport) int native_get(const char* key, char* buffer, int buffer_size) {
    if (!key || !buffer || buffer_size <= 0) return -1;
    
    auto it = storage.find(std::string(key));
    if (it == storage.end()) return -1;
    
    const std::string& value = it->second;
    if (value.size() >= static_cast<size_t>(buffer_size)) return -1;
    
    std::strcpy(buffer, value.c_str());
    return 0;
}

__declspec(dllexport) int native_delete(const char* key) {
    if (!key) return -1;
    
    auto it = storage.find(std::string(key));
    if (it == storage.end()) return -1;
    
    storage.erase(it);
    return 0;
}

}