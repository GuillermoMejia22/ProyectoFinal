#include <iostream> 
#include <string> 
 
int main() { 
    std::cin.tie(nullptr); 
    std::ios_base::sync_with_stdio(false); 
 
    std::string text, enlace, newText; 
    std::getline(std::cin, text); 
    std::getline(std::cin, enlace); 
  
    for (char c : text) { 
        newText += c; 
        if (c == '.') { 
            newText += "\\n"; 
        } 
    } 
 
    newText += "FUENTE: " + enlace; 
    std::cout << newText; 
    return 0; 
} 