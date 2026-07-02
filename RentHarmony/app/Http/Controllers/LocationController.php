<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Location;
use App\Models\District;

class LocationController extends Controller
{
    public function location()
    {
        $dist = District::all();
        return view('Admin.location', compact('dist'));
    }
    public function location_insert(Request $request)
    {
            Location::create([
             'locationname' => $request->locationname,
             'districtid'=>$request->districtid
         ]);
          return back()->with('success', 'Location Added Successfully');
    }
    public function location_view()
    {
        $dist=District::all();
        $loc = Location::all();
        return view('Admin.locationview', compact('dist','loc'));
    }
    public function getloc($districtid)
    {
        $pgm = Location::with('dist')->where('districtid', $districtid)->get();
        return response()->json($pgm);
    }
    public function deleteloc($locationid)
    {
        $loc = Location::find($locationid);
        if($loc){
            $loc->delete();
            return redirect()->route('location_view')->with('success','Location Deleted Successfully');
        }
    }
    public function updateloc($locationid)
    {
        $loc=Location::findOrFail($locationid);
        return view('Admin.updateloc',compact('loc'));
    }

      public function updateloctable(Request $request, Location $loc)
    {

    $loc->update([
        'locationname' => $request->locationname,
    ]);

    return redirect()->route('location_view')->with('success', 'Location Updated Successfully');
    }

}
