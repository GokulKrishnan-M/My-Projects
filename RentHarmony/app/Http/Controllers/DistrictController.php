<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\District;

class DistrictController extends Controller
{
     public function district()
    {
        return view('Admin.district');
    }

    public function district_insert(Request $request)
    {
            District::create([
             'districtname' => $request->districtname,
         ]);
          return back()->with('success', 'District Added Successfully');
    }
     public function districtview()
    {
        return view('Admin.viewdistrict');
    }

    public function viewdistrict()
    {
        $dist=District::all();

        return view('Admin.districtview',compact('dist'));
    }

    public function deletedist($districtid)
    {
        $dist = District::find($districtid);
        if($dist){
            $dist->delete();
            return redirect()->route('viewdistrict')->with('success','District Deleted Successfully');
        }
    }
    public function updatedist($districtid)
    {
        $dist=District::findOrFail($districtid);
        return view('Admin.updatedist',compact('dist'));
    }

      public function updatedisttable(Request $request, District $dist)
    {

    $dist->update([
        'districtname' => $request->districtname,
    ]);

    return redirect()->route('viewdistrict')->with('success', 'District Updated Successfully');
    }
}
