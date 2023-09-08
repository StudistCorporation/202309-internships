window.onload = function() {
  fetch('test-job-team-a.json')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {

      // トランスクリプトを「。」で区切って配列に格納      
      const transcriptArray = data.results.transcripts[0].transcript.split('。');

      // HTMLのul要素を取得
      const transcriptList = document.getElementById('transcriptList');
      
      // 各トランスクリプトをul要素に追加
      let stepNumber = 1;
      
      transcriptArray.forEach(transcript => {
        if (transcript) {  // 空の文字列を除外
          const listItem = document.createElement('li');
          listItem.textContent = `ステップ${stepNumber}: ${transcript}。`;  // ステップ番号を追加して表示
          transcriptList.appendChild(listItem);
          stepNumber++;  // ステップ番号をインクリメント
        }
      });

      // start_times = data.results.items[1].start_time
      // console.log(start_times);

    })
    .catch(error => {
      console.error('Error:', error);
    });
}



