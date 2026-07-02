<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('instruments', function (Blueprint $table) {
            $table->bigIncrements('instid');
            $table->string('instname');
            $table->string('image');
            $table->string('desc');
            $table->integer('ppd');
            $table->integer('stock');
            $table->string('status');
            $table->unsignedBigInteger('subcatid')->nullable();
            $table->index('subcatid');
            $table->foreign('subcatid')->references('subcategories')->on('subcategories')->onDelete('cascade');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('instruments');
    }
};
