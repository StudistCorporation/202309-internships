package main

import (
	"bufio"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

// 引数で指定したファイルをs3にアップロードしてくれます
// awsの認証情報とかは、~/.aws/configとかからよしなにとってきてくれるみたい
// リージョンや送信先のbucket名とか、keyの名前は固定してます
// アップロード成功すると、アップロード先のリンクを出力します

func main() {
	regionName := "ap-northeast-1"
	profileName := "default"
	bucketName := "hakone-test-input"
	key := "target-movie.mp4"

	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("> ")
	scanner.Scan()
	fileName := scanner.Text()

	sess := session.Must(session.NewSession(&aws.Config{
		Region:      aws.String(regionName),
		Credentials: credentials.NewSharedCredentials("", profileName),
	}))

	uploader := s3manager.NewUploader(sess)

	file, err := os.Open(fileName)
	if err != nil {
		log.Printf("Couldn't open file %v to upload. Here's why: %v\n", fileName, err)
	}
	defer file.Close()

	result, err := uploader.Upload(&s3manager.UploadInput{
		Bucket: aws.String(bucketName),
		Key:    aws.String(key),
		Body:   file,
	})
	if err != nil {
		log.Fatalf("failed to upload: %v", err)
	} else {
		fmt.Println("upload success", result.Location)
	}
}
