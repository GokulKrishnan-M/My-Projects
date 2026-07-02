@extends('layouts.adminmaster')
@section('content')

<!-- Include jQuery -->
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>

<!-- AJAX Script to Fetch Subcategories Based on Category -->
<script>
    $(document).ready(function () {
        $('#catid').change(function () {
            var catid = $(this).val();
            if (catid) {
                $.ajax({
                    url: '/getsubcatid/' + catid,
                    type: 'GET',
                    success: function (data) {
                        $('#subcategory').empty();
                        $('#subcategory').append('<option value="">Select a Subcategory</option>');
                        $.each(data, function (key, value) {
                            $('#subcategory').append('<option value="' + value.subcatid + '">' + value.subcatname + '</option>');
                        });
                    },
                    error: function () {
                        alert('Unable to fetch subcategories. Please try again later.');
                    }
                });
            } else {
                $('#subcategory').empty().append('<option value="">Select a Subcategory</option>');
            }
        });
    });
</script>

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">District Insert</h4>
                  <p class="card-description">
                    Instrument Details
                  </p>
                  <form  class="forms-sample" action="{{route('instinsert')}}" method="post" enctype="multipart/form-data">
                     @csrf
                    <div class="mb-4">
                      <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">SUBCATEGORY NAME</label><br>
                      <select class="form-control" name="catid" id="catid">
                      <option value="">-- Select Category Name --</option>
                       @foreach($inst as $d)
                        <option value="{{ $d->catid }}">
                            {{ $d->catname}}
                        </option>
                       @endforeach
                      </select>
                    </div>

                                       <div class="form-group">
                       <label for="subcategoryid">Subcategory</label>
                       <select name="subcategoryid" id="subcategory" required class="form-control">
                           <option value="">Select a subcategory</option>
                       </select>
                        </div>

                    <div class="form-group">
                      <label for="exampleInputName1"> Instrument Name</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="instname">
                      @error('instname')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1">Instrument Image</label>
                      <input type="file" class="form-control" id="exampleInputName1" name="image">
                      @error('image')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1">Desciption</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Description" name="desc">
                      @error('desc')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1">Price Per Day</label>
                      <input type="number" class="form-control" id="exampleInputName1" placeholder="Price Per Day" name="ppd">
                      @error('ppd')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1">Stock</label>
                      <input type="number" class="form-control" id="exampleInputName1" placeholder="Stock" name="stock">
                      @error('stock')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
                    </div>

                    
                    <button type="submit" class="btn btn-primary mr-2">Submit</button>
                   
                  </form>
                   @if (session('success'))
                  <script>
                    alert('{{session('success') }}')
                  </script>
                  @endif
                </div>
              </div>
            </div>

            @endsection