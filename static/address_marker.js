// JSON API의 URL
const apiUrl = 'http://localhost:5100/data_test';

// Fetch를 사용하여 데이터 가져오기
fetch(apiUrl)
  .then(response => response.json())
  .then(result => {
    const dataList = result.data;

    // 카카오맵 초기화
    const mapContainer = document.getElementById('map');
    const options = {
      center: new kakao.maps.LatLng(35.147206359654085, 129.0119992573746), // 초기 지도 중심 좌표 (서울)
      level: 5, // 초기 지도 확대 레벨
    };
    const map = new kakao.maps.Map(mapContainer, options);

    // 주소를 좌표로 변환하여 마커 생성 및 표시
    const geocoder = new kakao.maps.services.Geocoder();

    dataList.forEach(data => {
      const address = data.address;
      const name = data.name;

      geocoder.addressSearch(address, function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
          const markerPosition = new kakao.maps.LatLng(result[0].y, result[0].x);

          // 마커 생성
          const marker = new kakao.maps.Marker({
            position: markerPosition,
            title: name,
          });

          // 마커 지도에 표시
          marker.setMap(map);

          // 모든 마커가 표시되도록 지도의 범위 설정
          const bounds = new kakao.maps.LatLngBounds();
          bounds.extend(markerPosition);
          map.setBounds(bounds);
        }
      });
    });
  })
  .catch(error => {
    // 오류 처리
    console.error('데이터 가져오기 오류:', error);
  });