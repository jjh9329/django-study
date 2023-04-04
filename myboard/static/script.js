// 1. 글쓰기와 수정에서 쓸 수 있는 함수
// 제목이 비어있거나 또는 5글자 이하라면 경고창 표시하고 진행 멈춤
// 글 내용이 비어있거나 10 글자 이하라면 경고창 표시하고 진행멈춤
// 제목이나 글 내용에 바보,멍청이,한조 들어있으면 경고창 표시하고 진행멈춤
$(document).ready(function () {
  //alert("script연결")
});
function abcd() {
  let titleValue = document.getElementById('title').value.trim();
  let text = document.getElementById('content').value.trim(); //안되면 text
  let badWords = ['바보','멍청이','한조']
  if (titleValue.length <= 5) {
    alert("제목 5글자 이하");
    return false;
  }
  for (let i = 0; i < badWords.length; i++){
    if (titleValue.includes(badWords[i]) || text.includes(badWords[i])) {
      alert(badWords[i] + "는 사용불가");
      return false;
    }
  }
  if(text.length <= 10) {
    alert("내용이 10글자 이하");
    return false;
  }
}
// 2. 댓글에서 쓸 수 있는 함수
// 댓글 창 비어있으면 경고창 표시
