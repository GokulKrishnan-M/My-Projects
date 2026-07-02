@extends('layouts.adminmaster')
@section('content')
<br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Category Insert</h4>
                  <p class="card-description">
                    Insert your Category Information
                  </p>
                  <form action="{{route('update_inst',$instid->instid)}}" method="post" enctype="multipart/form-data">
                     @csrf
                    <div class="form-group">
                      <label for="exampleInputName1"> Instrument Name</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="instname" value="{{ $instid->instname }}">
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1">Instrument Image</label>
                       <img src="{{ asset('/uploads/' . $instid->image) }}" class="h-20 w-20 object-cover rounded shadow" alt="Image" 
 style="height: 100px;width:100px;">
                    </div>
                    <input type="hidden" class="form-control" id="exampleInputName1" placeholder="Name" name="oldimage" value="{{ $instid->image }}">

                    <input type="file" name="image" class="focus:shadow-primary-outline dark:bg-slate-850 dark:text-white text-sm leading-5.6 ease block w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 outline-none transition-all placeholder:text-gray-500 focus:border-blue-500 focus:outline-none" /> <br>
                    <div class="form-group">
                      <label for="exampleInputName1">Desciption</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Description" name="desc" value="{{ $instid->desc }}">
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1">Price Per Day</label>
                      <input type="number" class="form-control" id="exampleInputName1" placeholder="Price Per Day" name="ppd" value="{{ $instid->ppd }}">
                    </div>
                    
                    <div class="form-group">
                      <label for="exampleInputName1">Stock</label>
                      <input type="number" class="form-control" id="exampleInputName1" placeholder="Stock" name="stock" value="{{ $instid->stock }}">
                    </div>
                    

                    
                    <button type="submit" class="btn btn-primary mr-2">Submit</button>
                   
                   
                  </form>
                  </div>


                  
                   @if (session('success'))
                  <script>
                    alert('{{session('success') }}')
                  </script>
                  @endif
                </div>
              </div>
              </div>
           </div>
<br><br><br>
</div></div></div>
@endsection