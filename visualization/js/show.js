var getJSON = function(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.responseType = 'json';
  xhr.onload = function() {
    var status = xhr.status;
    if (status == 200) {
      callback(null, xhr.response);
    } else {
      callback(status);
    }
  };
  xhr.send();
};
var init = function(balls) {
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 50 );
  camera.position.z = 30;

  var renderer = new THREE.WebGLRenderer( { antialias: true } );
  renderer.setPixelRatio( window.devicePixelRatio );
  renderer.setSize( window.innerWidth, window.innerHeight );
  renderer.setClearColor( 0x000000, 1 );
  document.body.appendChild( renderer.domElement );

  var orbit = new THREE.OrbitControls( camera, renderer.domElement );

  var lights = [];
  lights[ 0 ] = new THREE.PointLight( 0xffffff, 1, 0 );
  lights[ 1 ] = new THREE.PointLight( 0xffffff, 1, 0 );
  lights[ 2 ] = new THREE.PointLight( 0xffffff, 1, 0 );

  lights[ 0 ].position.set( 0, 200, 0 );
  lights[ 1 ].position.set( 100, 200, 100 );
  lights[ 2 ].position.set( - 100, - 200, - 100 );

  scene.add( lights[ 0 ] );
  scene.add( lights[ 1 ] );
  scene.add( lights[ 2 ] );

  var mesh = new THREE.Object3D();

  mesh.add( new THREE.LineSegments(

    new THREE.Geometry(),

    new THREE.LineBasicMaterial( {
      color: 0xffffff,
      transparent: true,
      opacity: 0.5
    } )

  ) );
  cubeMaterial = new THREE.MeshPhongMaterial( {
    color: 0x156289,
    emissive: 0x072534,
    side: THREE.DoubleSide,
    shading: THREE.FlatShading,
    opacity: 0.4,
    transparent: true
  } )
  cubeGeometry = new THREE.BoxGeometry( 20, 20, 20 )
  cubeGeometry.translate(0, 0, 0)
  var cube = new THREE.Mesh(
    cubeGeometry,
    cubeMaterial
  );
  mesh.add( cube );

  balls.forEach(function(ball) {
    ball3D = new THREE.SphereGeometry(
      ball.radius / 10, 100, 100
    )
    ball.center.x -= 100;
    ball.center.x /= 10;
    ball.center.y -= 100;
    ball.center.y /= 10;
    ball.center.z -= 100;
    ball.center.z /= 10;
    ball3D.translate ( ball.center.x, ball.center.y, ball.center.z )

    mesh.add( new THREE.Mesh(
      ball3D,

      new THREE.MeshPhongMaterial( {
        color: 0x156289,
        emissive: 0x072534,
        side: THREE.DoubleSide,
        shading: THREE.FlatShading
      } )
    ) );
  })

  scene.add( mesh );

  var prevFog = false;


  var render = function () {

    requestAnimationFrame( render );

    mesh.rotation.x += 0.005;
    mesh.rotation.y += 0.005;

    renderer.render( scene, camera );

  };
  render()

  window.addEventListener( 'resize', function () {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

  }, false );
}

getJSON('/json-exports/3d.json', function (status, response) {
  init(response);
})
