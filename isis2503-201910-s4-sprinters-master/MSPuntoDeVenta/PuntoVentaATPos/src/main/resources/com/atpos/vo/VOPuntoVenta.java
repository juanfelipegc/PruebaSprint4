package com.atpos.vo;

public class VOPuntoVenta 
{
	private String direccion;
	private String negocio;
	
	public VOPuntoVenta(String direccion, String negocio) 
	{
		this.direccion = direccion;
		this.negocio = negocio;
	}
	
	public VOPuntoVenta()
	{
		//
	}

	public String getDireccion() {
		return direccion;
	}

	public void setDireccion(String direccion) {
		this.direccion = direccion;
	}

	public String getNegocio() {
		return negocio;
	}

	public void setNegocio(String negocio) {
		this.negocio = negocio;
	}
	
	
	
}