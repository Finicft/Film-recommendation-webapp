//  Based on https://stackoverflow.com/questions/9826253/performance-issues-using-images-with-arbor-js
//  main.js
//
//  A project template for using arbor.js
//

(function($){

  function demote(node,sys,parent){
    var parent_edges = sys.getEdgesTo(node);
    node.data.level = parent.data.level+1;
    if(parent_edges.length==1 && parent_edges[0].source.data.level==1){
      sys.pruneEdge(parent_edges[0]);
      demote(parent_edges[0].source,sys,node);
      sys.addEdge(node,parent_edges[0].source, {length:.5});
    }
    else{
      var children_edges = sys.getEdgesFrom(node);
      children_edges.forEach(function(child_edge) {
        demote(child_edge.target,sys,node);
      });
    }
  }

  function promote(node,sys,parent){
    node.data.level = parent.data.level+1;
    var children_edges = sys.getEdgesFrom(node);
    children_edges.forEach(function(child_edge) {
      promote(child_edge.target,sys,node);
    });
    if(node.data.level==2){
      console.log("Get data");
    }
  }

  function handleClick({node},sys){
    if(node.data.level==1){
      console.log("Yay!");
    }
    else{
      node.data.level=1
      var parent_edge = sys.getEdgesTo(node)[0];
      var children_edges = sys.getEdgesFrom(node);
      sys.pruneEdge(parent_edge);
      demote(parent_edge.source,sys,node);
      sys.addEdge(node,parent_edge.source, {length:.5});
      children_edges.forEach(function(child_edge) {
        promote(child_edge.target,sys,node);
      });
    }
  }

  function crop(image){
    var canvas = document.createElement('canvas'),
    ctx = canvas.getContext('2d'),
    startX = 0,
    startY = 0
    
    canvas.width=image.width
    canvas.height=image.height

    ctx.drawImage(image, 0, (image.height-image.width)/2);

    ctx.fillStyle = '#fff';
    ctx.globalCompositeOperation = 'destination-in';
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, canvas.width / 2, 0, Math.PI * 2, true);
    ctx.closePath();
    ctx.fill();

    return canvas;
  }

  arbor.Graphics = Graphics;
	var Renderer = function(canvas){
      var canvas = $(canvas).get(0)
      var ctx = canvas.getContext("2d");
      var gfx = arbor.Graphics(canvas)
      var particleSystem = null
  
      var that = {
        init:function(system){
          particleSystem = system
          system.screen({size:{width:$(canvas).width(), height:$(canvas).height()},
          padding:[0,0,0,0]})
          particleSystem.screenPadding(50)
          that.resize()
          that.initMouseHandling()
          
        },
        resize:function(){
          canvas.width = $(window).width()
          canvas.height = 0.95*$(window).height()
          particleSystem.screen({size:{width:canvas.width, height:canvas.height}})
          _vignette = null
        },
        redraw:function(){
          if (!particleSystem) return
  
          gfx.clear() // convenience ƒ: clears the whole canvas rect

          that.resize()
          var nodeBoxes = {};
          particleSystem.eachNode(function(node,pt){
            var label = node.data.label||"";
            var w = ctx.measureText(""+label).width + 10;
            if (node.data.shape=='dot'){
              gfx.oval(pt.x-w/2, pt.y-w/2, w,w, {fill:ctx.fillStyle})
              nodeBoxes[node.name] = [pt.x-w/2, pt.y-w/2, w,w]
            }else{
              gfx.rect(pt.x-w/2, pt.y-10, w,20, 4, {fill:ctx.fillStyle})
              nodeBoxes[node.name] = [pt.x-w/2, pt.y-11, w, 22]
            }
          });


          // draw the edges
          particleSystem.eachEdge(function(edge, pt1, pt2){
            // edge: {source:Node, target:Node, length:#, data:{}}
            // pt1:  {x:#, y:#}  source position in screen coords
            // pt2:  {x:#, y:#}  target position in screen coords
  
            var weight = edge.data.weight
            var color = edge.data.color
  
            if (!color || (""+color).match(/^[ \t]*$/)) color = null
  
            // find the start point
            var tail = intersect_line_box(pt1, pt2, nodeBoxes[edge.source.name])
            var head = intersect_line_box(tail, pt2, nodeBoxes[edge.target.name])
  
            ctx.save() 
              ctx.beginPath()
              ctx.lineWidth = (!isNaN(weight)) ? parseFloat(weight) : 1
              ctx.strokeStyle = (color) ? color : "#cccccc"
              ctx.fillStyle = null
  
              ctx.moveTo(tail.x, tail.y)
              ctx.lineTo(head.x, head.y)
              ctx.stroke()
            ctx.restore()
  
            // draw an arrowhead if this is a -> style edge
            if (edge.data.directed){
              ctx.save()
                // move to the head position of the edge we just drew
                var wt = !isNaN(weight) ? parseFloat(weight) : 1
                var arrowLength = 6 + wt
                var arrowWidth = 2 + wt
                ctx.fillStyle = (color) ? color : "#cccccc"
                ctx.translate(head.x, head.y);
                ctx.rotate(Math.atan2(head.y - tail.y, head.x - tail.x));
  
                // delete some of the edge that's already there (so the point isn't hidden)
                ctx.clearRect(-arrowLength/2,-wt/2, arrowLength/2,wt)
  
                // draw the chevron
                ctx.beginPath();
                ctx.moveTo(-arrowLength, arrowWidth);
                ctx.lineTo(0, 0);
                ctx.lineTo(-arrowLength, -arrowWidth);
                ctx.lineTo(-arrowLength * 0.8, -0);
                ctx.closePath();
                ctx.fill();
              ctx.restore()
            }
          })

          // draw the nodes & save their bounds for edge drawing
          particleSystem.eachNode(function(node, pt){
            // node: {mass:#, p:{x,y}, name:"", data:{}}
            // pt:   {x:#, y:#}  node position in screen coords
            
            var level = node.data.level;

            var baseWidth=67;
            var baseHeight=98;

            if(level==1){
              if(node.data.width<=baseWidth*2){
                node.data.width+= (baseWidth)/100;
                node.data.height+= (baseHeight)/100;
              }
            } else if(level==2){
              if(node.data.width>=baseWidth*3/2+(baseWidth)/100){
                node.data.width-= (baseWidth)/100;
                node.data.height-= (baseHeight)/100;
              }
              else if(node.data.width<=baseWidth*3/2-(baseWidth)/100){
                node.data.width+= (baseWidth)/100;
                node.data.height+= (baseHeight)/100;
              }
            } else if(level==3){
              if(node.data.width>=baseWidth+(baseWidth)/100){
                node.data.width-= (baseWidth)/100;
                node.data.height-= (baseHeight)/100;
              }
              else if(node.data.width<=baseWidth-(baseWidth)/100){
                node.data.width+= (baseWidth)/100;
                node.data.height+= (baseHeight)/100;
              }
            } else{
              if(node.data.width>30){
                node.data.width-=(baseWidth)/100;
                node.data.height-=(baseHeight)/100;
              }
              else{
                particleSystem.pruneNode(node);
              }
            }

            // Load extra info
            var imageH = node.data.height;
            var imageW = node.data.width;
            var radius = imageW;
  
            // determine the box size and round off the coords if we'll be 
            // drawing a text label (awful alignment jitter otherwise...)
            var label = node.data.label||""
            var w = ctx.measureText(""+label).width + 10
            if (!(""+label).match(/^[ \t]*$/)){
              pt.x = Math.floor(pt.x)
              pt.y = Math.floor(pt.y)
            }else{
              label = null
            }
  
            // draw a rectangle centered at pt
            if (node.data.color) ctx.fillStyle = node.data.color
            else ctx.fillStyle = "rgba(0,0,0,.2)"
            if (node.data.color=='none') ctx.fillStyle = "white"
  
  
            // draw the text
            if (label){
              ctx.font = "12px Helvetica"
              ctx.textAlign = "center"
              ctx.fillStyle = "white"
              if (node.data.color=='none') ctx.fillStyle = '#333333'
              ctx.fillText(label||"", pt.x, pt.y+4)
              ctx.fillText(label||"", pt.x, pt.y+4)
            }
            

            if (node.data.imageUrl){
              // Custom image loading function
              if(node.data.image==null){
                var pic = new Image();
                pic.onload = function() {  
                  node.data.image=crop(pic);

                }
                pic.src = node.data.imageUrl;
              }
              else{
                ctx.drawImage(node.data.image, pt.x-(radius/2), pt.y-(radius/2), imageW, imageH);
              }
            }
          })    			
  
  
  
        },
        initMouseHandling:function(){
          // no-nonsense drag and drop (thanks springy.js)
          selected = null;
          nearest = null;
          var dragged = null;
  
          // set up a handler object that will initially listen for mousedowns then
          // for moves and mouseups while dragging
          var handler = {
            clicked:function(e){
              var pos = $(canvas).offset();
              _mouseP = arbor.Point(e.pageX-pos.left, e.pageY-pos.top)
              selected = nearest = dragged = particleSystem.nearest(_mouseP);
  
              if (dragged.node !== null) dragged.node.fixed = true
  
              nearest.dragged = false;

              $(canvas).bind('mousemove', handler.dragged)
              $(window).bind('mouseup', handler.dropped)
  
              return false
            },
            dragged:function(e){
              nearest.dragged = true;
              var old_nearest = nearest && nearest.node._id
              var pos = $(canvas).offset();
              var s = arbor.Point(e.pageX-pos.left, e.pageY-pos.top)
              
              var p = particleSystem.fromScreen(s)

              if (!nearest) return
              if (dragged !== null && dragged.node !== null){
                dragged.node.p = p
              }

              
  
              return false
            },
  
            dropped:function(e){
              if (dragged===null || dragged.node===undefined ){
                return
              }
              if(nearest &&!nearest.dragged){
                handleClick(nearest,particleSystem);
              }
              if (dragged.node !== null) dragged.node.fixed = false
              dragged.node.tempMass = 1000
              dragged = null
              selected = null
              $(canvas).unbind('mousemove', handler.dragged)
              $(window).unbind('mouseup', handler.dropped)
              _mouseP = null
              return false
            }
          }
          $(canvas).mousedown(handler.clicked);
  
        }
  
      }
  
      // helpers for figuring out where to draw arrows (thanks springy.js)
      var intersect_line_line = function(p1, p2, p3, p4)
      {
        var denom = ((p4.y - p3.y)*(p2.x - p1.x) - (p4.x - p3.x)*(p2.y - p1.y));
        if (denom === 0) return false // lines are parallel
        var ua = ((p4.x - p3.x)*(p1.y - p3.y) - (p4.y - p3.y)*(p1.x - p3.x)) / denom;
        var ub = ((p2.x - p1.x)*(p1.y - p3.y) - (p2.y - p1.y)*(p1.x - p3.x)) / denom;
  
        if (ua < 0 || ua > 1 || ub < 0 || ub > 1)  return false
        return arbor.Point(p1.x + ua * (p2.x - p1.x), p1.y + ua * (p2.y - p1.y));
      }
  
      var intersect_line_box = function(p1, p2, boxTuple)
      {
        var p3 = {x:boxTuple[0], y:boxTuple[1]},
            w = boxTuple[2],
            h = boxTuple[3]
  
        var tl = {x: p3.x, y: p3.y};
        var tr = {x: p3.x + w, y: p3.y};
        var bl = {x: p3.x, y: p3.y + h};
        var br = {x: p3.x + w, y: p3.y + h};
  
        return intersect_line_line(p1, p2, tl, tr) ||
              intersect_line_line(p1, p2, tr, br) ||
              intersect_line_line(p1, p2, br, bl) ||
              intersect_line_line(p1, p2, bl, tl) ||
              false
      }
  
      return that
    }   

  $(document).ready(function(){
    var sys = arbor.ParticleSystem(300, 400, 1) // create the system with sensible repulsion/stiffness/friction
    sys.parameters({gravity:true}) // use center-gravity to make the graph settle nicely (ymmv)
    sys.renderer = Renderer("#viewport") // our newly created renderer will have its .init() method called shortly by sys...

    // add some nodes to the graph and watch it go...
    sys.addNode('a', {
    mass: 0.5,
    imageUrl: 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_UX182_CR0,0,182,268_AL_.jpg',
    width: 67*2,
    height: 98*2,
    level: 1})

    sys.addNode('b', {
    mass: 0.5,
    imageUrl: 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_UX182_CR0,0,182,268_AL_.jpg',
    width: 67*3/2,
    height: 98*3/2,
    level: 2})
    sys.addEdge('a','b', {length:.5})

    sys.addNode('c', {
    mass: 0.5,
    imageUrl: 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_UX182_CR0,0,182,268_AL_.jpg',
    width: 67*3/2,
    height: 98*3/2,
    level: 2})
    sys.addEdge('a','c', {length:.5})
    
    sys.addNode('d', {
    mass: 0.5,
    imageUrl: 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_UX182_CR0,0,182,268_AL_.jpg',
    width: 67*3/2,
    height: 98*3/2,
    level: 2})
    sys.addEdge('a','d', {length:.5})

    sys.addNode('e', {
      mass: 0.5,
      imageUrl: 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_UX182_CR0,0,182,268_AL_.jpg',
      width: 67,
      height: 98,
      level: 3})
      sys.addEdge('d','e', {length:.5})
    
    // or, equivalently:
    //
    // sys.graft({
    //   nodes:{
    //     f:{alone:true, mass:.25}
    //   }, 
    //   edges:{
    //     a:{ b:{},
    //         c:{},
    //         d:{},
    //         e:{}
    //     }
    //   }
    // })
    
  })

})(this.jQuery)