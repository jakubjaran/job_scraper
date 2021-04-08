const express = require('express')
const app = express()
const port = 3000

const fs = require('fs')

app.get('/', (req, res) => {
	let rawdata = fs.readFileSync('offers.json')
	let offers = JSON.parse(rawdata)
	res.send(offers)
})

app.listen(port, () => {
	console.log('server is running')
})
