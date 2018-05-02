package main

import (
	"encoding/json"
	"os"
	"log"
	"fmt"
	"bufio"
	"os/exec"
	"io"
)

func ReadLine(){
	
}

func main(){
	cmd = exec.Command("sxhkd")
	cmd.Start()
	stdin, err = cmd.StdinPipe()
	if err != nil {
		log.Fatal(err)
	}
	messages := make(chan map[string]string, 1)
	var blocks map[string]string
	reader := bufio.NewReader(os.Stdin)
	if _, err := reader.ReadString('\n'); err != nil {
		log.Fatal(err)
	}
	dec := json.NewDecoder(reader)
	if _, err := dec.Token(); err != nil {
		log.Fatal(err)
	}
	
	for dec.More() {
		var block map[string]string
		if val, ok := block["label"]; ok {
			blocks[val], _ = block["full_text"]
			messages <- blocks
		}
	}
	if _, err := dec.Token(); err != nil {
		log.Fatal(err)
	}
}
