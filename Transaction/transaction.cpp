#include<iostream>
#include<fstream>
#include<vector>
#include<string>
#include<unordered_map>
#include<unordered_set>
#include<sstream>

using namespace std;


vector<pair<string,string>> graphMake(const vector<vector<string>>& input) 
{
          vector<pair<string, string>> graph;
          vector<string> transactions, operations, values;
          int numSteps = input[0].size();
          int numTransactions = input.size();

          for (int j = 1; j < numSteps; ++j) 
          {
                    for (int i = 0; i < numTransactions; ++i) 
                    {
                              if (input[i][j] != "-" && input[i][j] != "COM") 
                              {
                                        string transaction = input[i][0];
                                        char operation = input[i][j][0];
                                        char value = input[i][j][2];

                                        for (size_t idx = 0; idx < transactions.size(); ++idx) 
                                        {
                                                  if (values[idx] == value && transaction != transactions[idx]) 
                                                  {
                                                            if (operations[idx] != operation || operation == 'W') 
                                                            {
                                                                      graph.push_back({transactions[idx], transaction});
                                                            }
                                                  }
                                        }
                                        transactions.push_back(transaction);
                                        operations.push_back(string(1, operation));
                                        values.push_back(string(1, value));
                              }
                    }
          }
          return graph;
}

bool cycleCheck(const vector<pair<string, string>>& graph) 
{
          unordered_map<string, vector<string>> adjList;


          for (const auto& edge : graph) 
          {
                    adjList[edge.first].push_back(edge.second);
          }

          unordered_set<string> visited, recStack;

   
          function<bool(const string&)> dfs = [&](const string& node) 
          {
                    if (recStack.count(node)) 
                              return true;
                    if (visited.count(node)) 
                              return false;

                    recStack.insert(node);
                    visited.insert(node);

                    for (const string& neighbor : adjList[node]) 
                    {
                              if (dfs(neighbor)) return true;
                    }

                    recStack.erase(node);
                    return false;
          };

          for (const auto& pair : adjList) 
          {
                    const string& node = pair.first;
                    if (!visited.count(node)) 
                    {
                              if (dfs(node)) return true;
                    }
          }

          return false;
}

int main() 
{         
          vector<vector<string>>input;
          ifstream file("input.csv");
          string line;

          while(getline(file, line)) 
          {
                    stringstream ss(line);
                    string value;
                    vector<string> row;
                    while(getline(ss,value,',')) 
                    {
                              row.push_back(value);
                    }
                    input.push_back(row);
          }
          file.close();

          vector<pair<string, string>> graph = graphMake(input);
          for (const auto& edge : graph) 
          {
                    cout << edge.first << " -> " << edge.second << endl;
          }

          if (cycleCheck(graph)) 
          {
                    cout << "Conflict" << endl;
          } 
          else 
          {
                    cout << "Parallel" << endl;
          }

          return 0;
}
