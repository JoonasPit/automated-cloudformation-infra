package main

import (
	"akefalos-api/helpers"
	"errors"
	"fmt"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func main() {
	lambda.Start(HandleRequest)
	fmt.Println("Hello")

}

// Test out returning not a basic af value with events.apiproxy.. More control over body etc
func HandleRequest(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	if request.HTTPMethod == "GET" {
		myStruct := helpers.ResponseStruct{Body: "foo", StatusCode: 200}
		ApiResponse := events.APIGatewayProxyResponse{Body: myStruct.Body, StatusCode: int(myStruct.StatusCode)}
		return ApiResponse, nil
	} else {
		myError := errors.New("Something wentWrong")
		ApiResponse := events.APIGatewayProxyResponse{Body: "This", StatusCode: 200}
		return ApiResponse, myError
	}
}
