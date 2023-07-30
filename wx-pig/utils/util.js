const formatTime = date => {
	const year = date.getFullYear()
	const month = date.getMonth() + 1
	const day = date.getDate()
	const hour = date.getHours()
	const minute = date.getMinutes()
	const second = date.getSeconds()

	return `${[year, month, day].map(formatNumber).join('-')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

const formatNumber = n => {
	n = n.toString()
	return n[1] ? n : `0${n}`
}

const getTimeLastWeek = last => {
	const year = last.getFullYear()
	const day = last.getDate()
	const ti = day - 7
	// const month6 = last.getMonth() + 1
	// const dayOfWeek = last.getDay() //今天本周的第几天  
	// 判断是否月初
	if (ti <= 0) {
		const month = last.getMonth() + 1 - 1
		const d = new Date(year, month, 0)
		const dayBig = d.getDate() //获取当月的所有天数
		const ti1 = dayBig + ti
		return [year, month, ti1].map(formatNumber).join('-')
	} else {
		const month = last.getMonth() + 1
		return [year, month, ti].map(formatNumber).join('-')
	}
}

module.exports = {
	formatTime,
	getTimeLastWeek
}