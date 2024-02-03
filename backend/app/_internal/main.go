package main

import (
	"fmt"
	"strings"
	"os"
	"bufio"

	xj "github.com/basgys/goxml2json"
)

func main() {
	in := bufio.NewReader(os.Stdin);
	line, err := in.ReadString('\n');
	if err != nil {
		panic("Unknown Error.");
	}

	xml := strings.NewReader(line);
	json, err := xj.Convert(xml);
	if err != nil {
		panic("Unknown error.");
	}

	fmt.Println(json.String());
}