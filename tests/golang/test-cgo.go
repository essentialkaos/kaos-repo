package main

// const int x = 42;
import "C"

import "fmt"

func main() {
	fmt.Println(int(C.x))
}
