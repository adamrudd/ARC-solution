#include "precompiled_stl.hpp"

using namespace std;

#include "utils.hpp"
#include "core_functions.hpp"
#include "image_functions.hpp"
#include "visu.hpp"
#include "read.hpp"

int main() {
  vector<Sample> sample = readAll("test", -1);
  cout << sample.size() << endl;
}

// From perplexity:
// #include "precompiled_stl.hpp"
// #include <filesystem>

// using namespace std;

// #include "utils.hpp"
// #include "core_functions.hpp"
// #include "image_functions.hpp"
// #include "visu.hpp"
// #include "read.hpp"

// int main() {
//   cout << "Starting count_tasks..." << endl;
//   cout << "Current working directory: " << filesystem::current_path() << endl;
  
//   string test_dir = "test";
//   cout << "Looking for tasks in directory: " << test_dir << endl;
  
//   vector<Sample> sample = readAll(test_dir, -1);
//   cout << "Number of tasks found: " << sample.size() << endl;
  
//   // Print the names of the first few task files (up to 5)
//   cout << "First few task files:" << endl;
//   for (size_t i = 0; i < min(sample.size(), size_t(5)); ++i) {
//     cout << sample[i].name << endl;
//   }
  
//   return 0;
// }
