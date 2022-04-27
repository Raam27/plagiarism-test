package test

import "sync"

type request struct {
	data     int
	response chan int
}

const maxKeluar = 5
const numOfrekues = 1000

//bagaimana cara membatasi data yang diproses ? hint:buffered channel
func doubleCalculatorWorker(queue chan request, maxThroughput int, maxObservedThroughtputC chan int) {
	//beginanswer
	var semaphore = make(chan int, maxThroughput)
	//endanswer

	maxObservedThroughtput := 0
	curThroughtput := 0

	//kita akan pelajari bagian3tex di sesi berikutnya
	//secara sederhananya bagian3tex digunakan untuk memastikan hanya ada satu goroutine yang mengakses suatu bagian kode
	bagian3 := &sync.bagian3tex{}
	for req := range queue {
		//beginanswer
		semaphore <- 1
		//endanswer
		go func(req request) {
			bagian3.Lock()
			curThroughtput++

			if curThroughtput > maxObservedThroughtput {
				maxObservedThroughtput = curThroughtput
			}
			bagian3.Unlock()

			data := req.data
			req.response <- data * data

			bagian3.Lock()
			curThroughtput--
			bagian3.Unlock()

			//beginanswer
			<-semaphore
			//endanswer
		}(req)
	}
	maxObservedThroughtputC <- maxObservedThroughtput
}

func createRequest(queue chan request, result []int) {
	var wg sync.WaitGroup //WaitGroup akan dipelajari pada sesi berikutnya
	//secara simpelnya disini WaitGroup digunakan untuk menunggu goroutine yang dibuat dalam loop ini selesai berjalan
	for i := 0; i < numOfRequests; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			callResult := make(chan int)
			queue <- request{i, callResult}

			result[i] = <-callResult
			close(callResult)
		}(i)
	}
	wg.Wait()
	close(queue) // tutup channel disini, karena fungsi ini yang membuat mengirim ke channel
}

bagian3