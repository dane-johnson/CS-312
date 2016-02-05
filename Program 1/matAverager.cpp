//Most of this code by Professor Mark McKenny
//Averaging algorithm by Dane Johnson
#include <sys/time.h>
#include <fstream>
#include <iostream>
#include <omp.h>
#include <cstdlib>
#include <sstream>
#include <list>
#include <string>

using namespace std;

typedef unsigned int ** val;

struct ordered_pair
{
	int x;
	int y;
	ordered_pair(){}
	ordered_pair(int init_x, int init_y)
	{
		x = init_x;
		y = init_y;
	}
};

double findmaxavg(val, const int&, const int&, list<ordered_pair>&);
double findlocalavg(val, const int&, const int&, const int&, const int&);

// a class to get more accurate time

class stopwatch{
	
private:
	double elapsedTime;
	double startedTime;
	bool timing;
	//returns current time in seconds
	double current_time( ) 
	{
		timeval tv;
		gettimeofday(&tv, NULL);
		double rtn_value = (double) tv.tv_usec;
		rtn_value /= 1e6;
		rtn_value += (double) tv.tv_sec;
		return rtn_value;
	}
	
public:
	stopwatch( ): elapsedTime( 0 ), startedTime( 0 ), timing( false )
	{
		
	}
	
	void start( )
	{
		if( !timing )
		{
			timing = true;
			startedTime = current_time( );
		}
	}
	
	void stop( )
	{
		if( timing )
		{
			elapsedTime +=  current_time( )-startedTime;
			timing = false;
		}
	}
	
	void resume( )
	{
		start( );
	}
	
	void reset( )
	{
		elapsedTime = 0;
		startedTime = 0;
		timing = false;
	}
	
	double getTime( )
	{
		return elapsedTime;
	}
};



// function takes an array pointer, and the number of rows and cols in the array, and 
// allocates and intializes the two dimensional array to a bunch of random numbers

void makeRandArray( unsigned int **& data, unsigned int rows, unsigned int cols, unsigned int seed )
{
	// allocate the array
	data = new unsigned int*[ rows ];
	for( unsigned int i = 0; i < rows; i++ )
	{
		data[i] = new unsigned int[ cols ];
	}
	
	// seed the number generator
	// you should change the seed to get different values
	srand( seed );
	
	// populate the array
	
	for( unsigned int i = 0; i < rows; i++ )
		for( unsigned int j = 0; j < cols; j++ )
		{
			data[i][j] = rand() % 10000 + 1; // number between 1 and 10000
		}
	
}

void getDataFromFile( unsigned int **& data, char fileName[], unsigned int &rows, unsigned int &cols )
{
	ifstream in;
	in.open( fileName );
	if( !in )
	{
		cerr << "error opening file: " << fileName << endl;
		exit( -1 );
	}
	
	in >> rows >> cols;
	data = new unsigned int*[ rows ];
	for( unsigned int i = 0; i < rows; i++ )
	{
		data[i] = new unsigned int[ cols ];
	}
	
	// now read in the data
	
	for( unsigned int i = 0; i < rows; i++ )
		for( unsigned int j = 0; j < cols; j++ )
		{
			in >> data[i][j];
		}
	
}


int main( int argc, char* argv[] ) 
{
	if( argc < 3 )
	{
		cerr<<" usage: exe [input data file] [num of threads to use] " << endl;
		
		cerr<<"or usage: exe rand [num of threads to use] [num rows] [num cols] [seed value]" << endl;
	}
	
	// read in the file
	unsigned int rows, cols, seed;
	unsigned int numThreads;
	unsigned int ** data;
	// convert numThreads to int
	{
		stringstream ss1;
		ss1 << argv[2];
		ss1 >> numThreads;
	}
	
	string fName( argv[1] );
	if( fName == "rand" )
	{
		{
			stringstream ss1;
			ss1 << argv[3];
			ss1 >> rows;
		}
		{
			stringstream ss1;
			ss1 << argv[4];
			ss1 >> cols;
		}
		{
			stringstream ss1;
			ss1 << argv[5];
			ss1 >> seed;
		}
		makeRandArray( data, rows, cols, seed );
	}
	else
	{
		getDataFromFile( data,  argv[1], rows, cols );
	}
	
		//cerr << "data: " << endl;
	 for( unsigned int i = 0; i < rows; i++ )
	 {
	 for( unsigned int j = 0; j < cols; j++ )
	 {
	 //cerr << "i,j,data " << i << ", " << j << ", ";
	 //cerr << data[i][j] << " ";
	 }
	 //cerr << endl;
	 }
	 //cerr<< endl;
	
	// tell omp how many threads to use
	omp_set_num_threads( numThreads );
	
	stopwatch S1;
	S1.start();
	
	double avg;
	list<ordered_pair> pairs;
	
	avg = findmaxavg(data, rows, cols, pairs);
	
	S1.stop();
	
	// print out the max value here
	
	cout << "largest average: " << avg << endl;
	cout << "found at cells: ";
	while(!pairs.empty())
	{
		ordered_pair curr = pairs.front();
		cout << "(" << curr.x << ", " << curr.y <<")  ";
		pairs.pop_front();
	}
	cout << endl;
	cerr << "elapsed time: " << S1.getTime( ) << endl;
}

//finds max average iteratively
double findmaxavg(val data, const int& rows, const int& cols, list<ordered_pair>& pairs)
{
	double max = findlocalavg(data, 0, 0, rows, cols); //set first value to max
	pairs.push_front(ordered_pair(0, 0));
	
	#pragma omp parallel for
	for(int i = 0; i < rows; i++)
	{
		for(int j = 0; j < cols; j++)
		{
			double test = findlocalavg(data, i, j, rows, cols); //get the local average
			if(test > max)
			{
				max = test; // if it's better, replace it
				pairs.clear();
				pairs.push_front(ordered_pair(i, j));
			} 
			else if (test == max)
			{
				pairs.push_back(ordered_pair(i, j));
			}				//They are the same, add this to the pairs
		}
	}
	
	return max;
}

//
double findlocalavg(val data, const int& i, const int& j, const int& rows, const int& cols)
{
	int nvals = 1, total = data[i][j]; //We have at least one value
	bool isTop = (j == 0), isBottom = (j + 1 == cols), isLeftEdge = (i == 0), isRightEdge = (i + 1 == rows);
	if(!isLeftEdge) //We're clear to the left
	{
		nvals++;
		total += data[i - 1][j];
		if(!isTop)//Top left clear
		{
			nvals++;
			total += data[i - 1][j - 1];
		}
		if(!isBottom)//Bottom left clear
		{
			nvals++;
			total += data[i - 1][j + 1];
		}
	}
	if(!isRightEdge) //We're clear to the right
	{
		nvals++;
		total += data[i + 1][j];
		if(!isTop)//Top right clear
		{
			nvals++;
			total += data[i + 1][j - 1];
		}
		if(!isBottom)//Bottom right clear
		{
			nvals++;
			total += data[i + 1][j + 1];
		}
	}
	if(!isTop) //Top clear
	{
		nvals++;
		total += data[i][j - 1];
	}
	if(!isBottom)
	{
		nvals++;
		total += data[i][j + 1];
	}
	
	return double(total) / nvals;
}


