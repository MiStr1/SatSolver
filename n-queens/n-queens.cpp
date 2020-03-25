#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

void reduce_nq_sat(int n) {
	vector<vector<int>> map;
	int k = 1;
	for (int i = 0; i < n; ++i) {
		map.push_back(vector<int>());
		for (int j = 0; j < n; ++j) {
			map[i].push_back(k);
			k++;
		}
	}

	vector<stringstream> output;
	output.push_back(stringstream());
	output[0] << "p cnf " << n * n << " ";
	int clauses = 0;
	for (int i = 0; i < n; ++i) {
		output.push_back(stringstream());
		clauses++;
		for (int j = 0; j < n; ++j) {
			output[clauses] << map[i][j] << " ";
		}
		output[clauses] << 0;
	}

	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n-1; ++j) {
			
			for (int l = j + 1; l < n; ++l) {
				output.push_back(stringstream());
				clauses++;
				output[clauses] <<-map[i][j] << " "<< -map[i][l] << " "<<0;
			}
		}
	}

	for (int j = 0; j < n; ++j) {
		for (int i = 0; i < n - 1; ++i) {
			for (int l = i + 1; l < n; ++l) {
				output.push_back(stringstream());
				clauses++;
				output[clauses] << -map[i][j] << " " << -map[l][j] << " " << 0;
			}
		}
	}

	for (int d = 0; d < n-1; ++d) {
		for (int i=0,j = d; i < n - 1&&j<n-1; ++i,++j) {
			for (int p = i + 1,r=j+1; p < n&&r<n; ++p,++r) {
				output.push_back(stringstream());
				clauses++;
				output[clauses] << -map[i][j] << " " << -map[p][r] << " " << 0;
			}
		}
	}

	for (int d = 1; d < n - 1; ++d) {
		for (int i = d, j = 0; i < n - 1 && j < n - 1; ++i, ++j) {
			for (int p = i + 1, r = j + 1; p < n&&r < n; ++p, ++r) {
				output.push_back(stringstream());
				clauses++;
				output[clauses] << -map[i][j] << " " << -map[p][r] << " " << 0;
			}
		}
	}

	for (int d = 1; d < n; ++d) {
		for (int i = 0, j = d; i <n-1 && j > 0; ++i, --j) {
			for (int p = i + 1, r = j - 1; p <n && r >= 0; ++p, --r) {
				output.push_back(stringstream());
				clauses++;
				output[clauses] << -map[i][j] << " " << -map[p][r] << " " << 0;
			}
		}
	}

	for (int d = 1; d < n-1; ++d) {
		for (int i = d, j = n-1; i < n-1 && j > 0; ++i, --j) {
			for (int p = i + 1, r = j - 1; p  < n && r >= 0; ++p, --r) {
				output.push_back(stringstream());
				clauses++;
				output[clauses] << -map[i][j] << " " << -map[p][r] << " " << 0;
			}
		}
	}

	output[0] << clauses;

	for (int i = 0; i < output.size();++i) {
		cout << output[i].str()<<endl;
	}
}

int main()
{
	int n;
	cin >> n;
	reduce_nq_sat(n);
	return 0;
}
