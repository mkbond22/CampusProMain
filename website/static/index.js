function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


// Sort data - using bubblesort
function sort(arr){
  for(var i = arr.length; i > 0; i--){      // i should be counting down from the end of arr
    for(var j = 0; j < i - 1; j++){         // now this loop only runs while j < i -- and i decreases every iteration
      console.log(arr);
      if(arr[j] > arr[j+1]){
        //SWAP!
        var temp = arr[j];
        arr[j] = arr[j+1];
        arr[j+1] = temp;
      }
    }
  }
  return arr;
}

