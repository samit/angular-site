var app = angular.module('LinMin', ['ngRoute', 'angularUtils.directives.dirPagination','nvd3']);
app.config(['$routeProvider', function($routeProvider){
	  $routeProvider
	  .when("/", {templateUrl:"dashboard.html"})
	  .when("/process", {templateUrl: "process.html", controller: "SidebarController"})
	  .when("/cpu", {templateUrl: "cpu.html", controller: "SidebarController"})
	  .when("/memory", {templateUrl: "mem_usage.html", controller: "SidebarController"})
	  .when("/addhost", {templateUrl: "host.html", controller: "SidebarController"})
	  .when("/alert", {templateUrl: "alert_noti.html", controller: "SidebarController"})
      .when("/system", {templateUrl: "system.html", controller: "SidebarController"})
     .when("/network", {templateUrl: "network.html", controller: "SidebarController"})

      .otherwise("/");
}]);




app.controller("SidebarController", function($scope){

});

app.controller("NavbarController", function($scope){
	$scope.mem=40;
	$scope.cpu=20;
	$scope.disk=60;
});

app.controller("PageController", function($scope, $http, $interval){
  var processdata = []; 
  $scope.reload = function (){
 	$http.get('../services/page_process.json').success(function(data){
  	$scope.processdata = data
  	for( var i =0; i<processdata.length; i++){
    		return processdata[i]
		}
	} );

			}
		$scope.reload();
       		$interval($scope.reload, 5000);


  var majmin = [];
  $scope.reload =function(){
          $http.get('../services/pro_maj_min.json').success(function(data){
          $scope.majmin= data
          for (var i =0; i<majmin.length; i++){
           return majmin[i];
          }
       
      });
}
     $scope.reload();
     $interval($scope.reload, 5000);


  var disk_page = [];
   $scope.reload =function(){
          $http.get('../services/disk_usage.json').success(function(data){
          $scope.disk_page = data
          for (var i =0; i<disk_page.length; i++){
           return disk_page[i];
          } 
      });
}
     $scope.reload();
     $interval($scope.reload, 5000);

  var procs_page = [];
   $scope.reload =function(){
          $http.get('../services/procs_stat.json').success(function(data){
          $scope.procs_page =data
          for (var i =0; i<procs_page.length; i++){
           return procs_page[i];
          }

      });
}
     $scope.reload();
     $interval($scope.reload, 5000);




  var iopage= [];
  $scope.reload = function(){

         $http.get('../services/io_per_process.json ').success(function(data){
            $scope.iopage = data;
             for (var i= 0; i<iopage.length; i++){
              return iopage[i];

}

});

}

   $scope.reload();
   $interval($scope.reload, 5000);
  var ctxpage = [];
  $scope.reload =function(){
                $http.get('../services/ctxt.json').success(function(data){
                 $scope.ctxpage = data
                  for(i=0; i<ctxpage.length;i++){
		    return ctxpage[i];
}
});
}
                $scope.reload();
                $interval($scope.reload, 5000);
 var statm = [];
  $scope.reload= function(){
        $http.get('../services/statm.json').success(function(data){
           $scope.statm = data
          for(i=0; i<statm.length;i++){
           return statm[i];
}

});
}
$scope.reload();
                $interval($scope.reload, 5000);
   var iocons = [];
   $scope.reload =function(){
        $http.get('../services/io_con.json').success(function(data){
        $scope.iocons = data
        for(i=0; i<iocons.length;i++){
         return iocons[i];
}

});
}
$scope.reload();
                $interval($scope.reload, 5000);

   var tcpcon = [];
   $scope.reload= function(){
         $http.get('../services/tcpcon.json').success(function(data){
           $scope.tcpcon = data;
            for (i=0; i<tcpcon.length;i++){
             return tcpcon[i];
 
}
});
}
               $scope.reload();
               $interval($scope.reload, 5000);


   var cpucore = [];
   $scope.reload= function(){
         $http.get('../services/cpucore.json').success(function(data){
           $scope.cpucore = data;
            for (i=0; i<cpucore.length;i++){
             return cpucore[i];

}
});
}
               $scope.reload();
               $interval($scope.reload, 5000);

   var cpuper = [];
   $scope.reload= function(){
         $http.get('../services/cpuper.json').success(function(data){
           $scope.cpuper = data;
            for (i=0; i<cpuper.length;i++){
             return cpuper[i];

}
});
}
               $scope.reload();
               $interval($scope.reload, 5000);


 var vmstat = [];
   $scope.reload= function(){
         $http.get('../services/vmstat.json').success(function(data){
           $scope.vmstat = data;
            for (i=0; i<vmstat.length;i++){
             return vmstat[i];

}
});
}
               $scope.reload();
               $interval($scope.reload, 5000);
var mpstat = [];
   $scope.reload= function(){
         $http.get('../services/mpstat.json').success(function(data){
           $scope.mpstat = data;
            for (i=0; i<mpstat.length;i++){
             return mpstat[i];

}
});
}
               $scope.reload();
               $interval($scope.reload, 5000);

var topten = [];
   $scope.reload= function(){
         $http.get('../services/topten.json').success(function(data){
           $scope.topten = data;
           return topten
           console.log(topten)
});
}
               $scope.reload();
               $interval($scope.reload, 5000);

var cpuinfo = [];
   $scope.reload= function(){
         $http.get('../services/cpuinfo.json').success(function(data){
           $scope.cpuinfo = data;
           return topten
           console.log(topten)
});
}
               $scope.reload();
               $interval($scope.reload, 5000);



var memusage = [];
   $scope.reload= function(){
         $http.get('../services/memusage.json').success(function(data){
           $scope.memusage = data;
            for (i=0; i<memusage.length;i++){
             return memusage[i];

}
});
}
               $scope.reload();
               $interval($scope.reload, 5000);


var mempage = [];
   $scope.reload= function(){
         $http.get('../services/mempage.json').success(function(data){
           $scope.mempage = data;
            for (i=0; i<mempage.length;i++){
             return mempage[i];

}
});
}
               $scope.reload();
               $interval($scope.reload, 5000);

var pidcpu = [];
   $scope.reload= function(){
         $http.get('../services/pidstat.json').success(function(data){
           $scope.pidcpu = data;
            for (i=0; i<pidcpu.length;i++){
             return pidcpu[i];

}
});


}

	       
               $scope.reload();
               $interval($scope.reload, 5000);

$scope.options = {
            chart: {
                type: 'pieChart',
                height: 500,
                x: function(d){return d.PID;},
                y: function(d){return d.CPUper;},
                showLabels: true,
                duration: 500,
                labelThreshold:1,
                labelSunbeamLayout: true,
                legend: {
                    margin: {
                        top: 5,
                        right: 35,
                        bottom: 5,
                        left: 0
                    }
                }
            }
        };

//bar chart
$scope.memoptions = {
            chart: {
                type: 'pieChart',
                height: 500,
                x: function(d){return d.PID;},
                y: function(d){return d.VmRss;},
                showLabels: true,
                duration: 500,
                labelThreshold:1,
                labelSunbeamLayout: true,
                legend: {
                    margin: {
                        top: 5,
                        right: 35,
                        bottom: 5,
                        left: 0
                    }
                }
            }
        };

//Disk chart 

$scope.diskoptions = {
            chart: {
                type: 'pieChart',
                height: 500,
                x: function(d){return d.Filesystem;},
                y: function(d){return d.Used;},
                showLabels: true,
                duration: 500,
                labelThreshold:1,
                labelSunbeamLayout: true,
                legend: {
                    margin: {
                        top: 5,
                        right: 35,
                        bottom: 5,
                        left: 0
                    }
                }
            }
        };



//before last line
});

