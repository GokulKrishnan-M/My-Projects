<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Category;
use App\Models\Subcategory;
use App\Models\Instrument;


class InstrumentController extends Controller
{
    public function instrument()
    {
        $inst=Category::all();
        return view('Admin.instrument',compact('inst'));
    }
    public function getsubcatid($catid)
    {
        $pgm = Subcategory::with('cat')->where('catid', $catid)->get();
        return response()->json($pgm);
    }
     public function instinsert(Request $request)
    {
        $request->validate([
            'image'=>[
                'required', 
            ],
            'instname' => 'required',
            'desc' => 'required',
            'ppd' => 'required',
            'stock' => 'required',
    
        ]);
        $fileName = null;
        if ($request->hasFile('image')) {
         $image = $request->file('image');
         $fileName = $image->getClientOriginalName();
         $destinationPath = public_path('/uploads');
         $image->move($destinationPath, $fileName);
         }
            Instrument::create([
            'instname' => $request->instname,
            'image'=> $fileName,
            'desc' => $request->desc,
            'ppd' => $request->ppd,
            'stock' => $request->stock,
            'status' =>'available',
            'subcatid' => $request->subcategoryid,

         ]);
          return back()->with('success', 'Instrument Added Successfully');
    }
    public function instview()
    {
        $cat=Category::all();
        $inst = Instrument::all();
        return view('Admin.instrumentview', compact('cat','inst'));
    }
    public function getinst($subcatid)
    {
        $pgm = Instrument::with('subcat')->where('subcatid', $subcatid)->get();
        return response()->json($pgm);
    }
    public function deleteinst($instid)
    {
        $instid = Instrument::find($instid);
        if($instid){
            $instid->delete();
            return redirect()->route('instview')->with('success','Instrument Deleted Successfully');
        }
    }
     public function updateinst($instid)
    {
        $instid=Instrument::findOrFail($instid);
        return view('Admin.updateinstrument',compact('instid'));
    }
     public function update_inst(Request $request, Instrument $instid)
    {
 
        // Handle File Upload
        $fileName = $instid->image; // Default to existing photo
        if ($request->hasFile('image')) {
            $image = $request->file('image');
            $fileName = $image->getClientOriginalName();
            $destinationPath = public_path('/uploads');
            $image->move($destinationPath, $fileName);
        }
        else{
            $fileName = $request->oldimage;
        }

    $instid->update([
        'instname' => $request->instname,
        'desc' => $request->desc,
        'ppd' => $request->ppd,
        'stock' => $request->stock,
        'image'=>$fileName
    ]);

    return redirect()->route('instview')->with('success', 'Instrument Updated Successfully');
    }
}
