// Update the count down every 1 second
function countDownTimer(d_min) {

    // Get today's date and time
    var now = new Date().getMinutes();
    
    var countDownTime = now + d_min;  
  // Find the distance between now and the count down date
  var distance = countDownTime - now;

  // Time calculations for days, hours, minutes and seconds
  
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  console.log(minutes);
  // Display the result in the element with id="demo"
  return minutes + "m " + seconds + "s"
}

export { countDownTimer };