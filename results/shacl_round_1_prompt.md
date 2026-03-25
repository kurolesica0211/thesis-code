# Role: Expert Knowledge Graph Engineer — Correction Round
You are a specialized KGC engine performing a **correction pass**. Your previous extraction contained SHACL validation errors against the ontology.

# 1. Ontology (RDF/TTL)
---
<?xml version="1.0"?>
<rdf:RDF xmlns="http://www.co-ode.org/roberts/family-tree.owl#"
     xml:base="http://www.co-ode.org/roberts/family-tree.owl"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:fhkb="http://www.example.com/genealogy.owl#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
    <owl:Ontology rdf:about="http://www.co-ode.org/roberts/family-tree.owl">
        <rdfs:comment>A simple family relationships ontology and associated instances. the description is of the family of Robert Stevens and the intention is to use the minimal of asserted relationships and the maximum of inference. To do this  I&apos;ve used role chains, nominals and properties hierarchies.</rdfs:comment>
    </owl:Ontology>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Annotation properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://www.example.com/genealogy.owl#alsoKnownAs -->

    <owl:AnnotationProperty rdf:about="http://www.example.com/genealogy.owl#alsoKnownAs"/>
    


    <!-- http://www.example.com/genealogy.owl#formerlyKnownAs -->

    <owl:AnnotationProperty rdf:about="http://www.example.com/genealogy.owl#formerlyKnownAs"/>
    


    <!-- http://www.example.com/genealogy.owl#hasBirthYear -->

    <owl:AnnotationProperty rdf:about="http://www.example.com/genealogy.owl#hasBirthYear"/>
    


    <!-- http://www.example.com/genealogy.owl#hasDeathYear -->

    <owl:AnnotationProperty rdf:about="http://www.example.com/genealogy.owl#hasDeathYear"/>
    


    <!-- http://www.example.com/genealogy.owl#hasMarriageYear -->

    <owl:AnnotationProperty rdf:about="http://www.example.com/genealogy.owl#hasMarriageYear"/>
    


    <!-- http://www.example.com/genealogy.owl#knownAs -->

    <owl:AnnotationProperty rdf:about="http://www.example.com/genealogy.owl#knownAs"/>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Datatypes
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://www.co-ode.org/roberts/family-tree.owl#hasBirthYear -->

    <rdfs:Datatype rdf:about="http://www.co-ode.org/roberts/family-tree.owl#hasBirthYear"/>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Object Properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://www.example.com/genealogy.owl#hasAncestor -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasAncestor">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasRelation"/>
        <rdfs:subPropertyOf rdf:resource="http://www.w3.org/2002/07/owl#topObjectProperty"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isAncestorOf"/>
        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#TransitiveProperty"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasBrother -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasBrother">
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isBrotherOf"/>
        <owl:propertyDisjointWith rdf:resource="http://www.example.com/genealogy.owl#isChildOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasChild -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasChild">
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isChildOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasDaughter -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasDaughter">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasChild"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isDaughterOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasFather -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasFather">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasParent"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isFatherOf"/>
        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#FunctionalProperty"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Person"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Man"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasFemalePartner -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasFemalePartner">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasPartner"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isFemalePartnerIn"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Marriage"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Woman"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasHusband -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasHusband">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasSpouse"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isHusbandOf"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Man"/>
        <owl:propertyChainAxiom rdf:parseType="Collection">
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#isFemalePartnerIn"/>
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#hasMalePartner"/>
        </owl:propertyChainAxiom>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasMalePartner -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasMalePartner">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasPartner"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isMalePartnerIn"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Marriage"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Man"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasMother -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasMother">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasParent"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isMotherOf"/>
        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#FunctionalProperty"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Person"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Woman"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasParent -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasParent">
        <owl:equivalentProperty rdf:resource="http://www.example.com/genealogy.owl#isChildOf"/>
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasAncestor"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isParentOf"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Person"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Person"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasPartner -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasPartner">
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isPartnerIn"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Marriage"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Person"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasRelation -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasRelation">
        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#SymmetricProperty"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Person"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Person"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasSex -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasSex">
        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#FunctionalProperty"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Person"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Sex"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasSister -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasSister">
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isSisterOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasSon -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasSon">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasChild"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isSonOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasSpouse -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasSpouse">
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isSpouseOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#hasWife -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#hasWife">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasSpouse"/>
        <owl:inverseOf rdf:resource="http://www.example.com/genealogy.owl#isWifeOf"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Woman"/>
        <owl:propertyChainAxiom rdf:parseType="Collection">
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#isMalePartnerIn"/>
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#hasFemalePartner"/>
        </owl:propertyChainAxiom>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isAncestorOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isAncestorOf"/>
    


    <!-- http://www.example.com/genealogy.owl#isBloodrelationOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isBloodrelationOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#hasRelation"/>
        <rdfs:subPropertyOf rdf:resource="http://www.w3.org/2002/07/owl#topObjectProperty"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isBrotherOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isBrotherOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#isSiblingOf"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Man"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Person"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isChildOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isChildOf"/>
    


    <!-- http://www.example.com/genealogy.owl#isDaughterOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isDaughterOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#isChildOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isFatherOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isFatherOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#isParentOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isFemalePartnerIn -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isFemalePartnerIn"/>
    


    <!-- http://www.example.com/genealogy.owl#isHusbandOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isHusbandOf"/>
    


    <!-- http://www.example.com/genealogy.owl#isMalePartnerIn -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isMalePartnerIn"/>
    


    <!-- http://www.example.com/genealogy.owl#isMotherOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isMotherOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#isParentOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isParentOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isParentOf"/>
    


    <!-- http://www.example.com/genealogy.owl#isPartnerIn -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isPartnerIn"/>
    


    <!-- http://www.example.com/genealogy.owl#isSiblingOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isSiblingOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#isBloodrelationOf"/>
        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#SymmetricProperty"/>
        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#TransitiveProperty"/>
        <owl:propertyChainAxiom rdf:parseType="Collection">
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#hasParent"/>
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#isParentOf"/>
        </owl:propertyChainAxiom>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isSisterOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isSisterOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#isSiblingOf"/>
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Woman"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Person"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isSonOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isSonOf">
        <rdfs:subPropertyOf rdf:resource="http://www.example.com/genealogy.owl#isChildOf"/>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isSpouseOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isSpouseOf"/>
    


    <!-- http://www.example.com/genealogy.owl#isUncleOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isUncleOf">
        <rdfs:domain rdf:resource="http://www.example.com/genealogy.owl#Man"/>
        <rdfs:range rdf:resource="http://www.example.com/genealogy.owl#Person"/>
        <owl:propertyChainAxiom rdf:parseType="Collection">
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#isBrotherOf"/>
            <rdf:Description rdf:about="http://www.example.com/genealogy.owl#isParentOf"/>
        </owl:propertyChainAxiom>
    </owl:ObjectProperty>
    


    <!-- http://www.example.com/genealogy.owl#isWifeOf -->

    <owl:ObjectProperty rdf:about="http://www.example.com/genealogy.owl#isWifeOf"/>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Classes
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://www.example.com/genealogy.owl#Ancestor -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Ancestor">
        <owl:equivalentClass>
            <owl:Class>
                <owl:intersectionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="http://www.example.com/genealogy.owl#Person"/>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://www.example.com/genealogy.owl#isAncestorOf"/>
                        <owl:someValuesFrom rdf:resource="http://www.example.com/genealogy.owl#Person"/>
                    </owl:Restriction>
                </owl:intersectionOf>
            </owl:Class>
        </owl:equivalentClass>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Marriage"/>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Sex"/>
    </owl:Class>
    


    <!-- http://www.example.com/genealogy.owl#DomainEntity -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#DomainEntity"/>
    


    <!-- http://www.example.com/genealogy.owl#Female -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Female">
        <rdfs:subClassOf rdf:resource="http://www.example.com/genealogy.owl#Sex"/>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Male"/>
    </owl:Class>
    


    <!-- http://www.example.com/genealogy.owl#Male -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Male">
        <rdfs:subClassOf rdf:resource="http://www.example.com/genealogy.owl#Sex"/>
    </owl:Class>
    


    <!-- http://www.example.com/genealogy.owl#Man -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Man">
        <owl:equivalentClass>
            <owl:Class>
                <owl:intersectionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="http://www.example.com/genealogy.owl#Person"/>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://www.example.com/genealogy.owl#hasSex"/>
                        <owl:someValuesFrom rdf:resource="http://www.example.com/genealogy.owl#Male"/>
                    </owl:Restriction>
                </owl:intersectionOf>
            </owl:Class>
        </owl:equivalentClass>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Marriage"/>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Woman"/>
    </owl:Class>
    


    <!-- http://www.example.com/genealogy.owl#Marriage -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Marriage">
        <rdfs:subClassOf rdf:resource="http://www.example.com/genealogy.owl#DomainEntity"/>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Person"/>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Sex"/>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Woman"/>
    </owl:Class>
    


    <!-- http://www.example.com/genealogy.owl#Person -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Person">
        <owl:equivalentClass>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="http://www.example.com/genealogy.owl#Man"/>
                    <rdf:Description rdf:about="http://www.example.com/genealogy.owl#Woman"/>
                </owl:unionOf>
            </owl:Class>
        </owl:equivalentClass>
        <rdfs:subClassOf rdf:resource="http://www.example.com/genealogy.owl#DomainEntity"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="http://www.example.com/genealogy.owl#hasFather"/>
                <owl:someValuesFrom rdf:resource="http://www.example.com/genealogy.owl#Man"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="http://www.example.com/genealogy.owl#hasMother"/>
                <owl:someValuesFrom rdf:resource="http://www.example.com/genealogy.owl#Woman"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="http://www.example.com/genealogy.owl#hasSex"/>
                <owl:someValuesFrom rdf:resource="http://www.example.com/genealogy.owl#Sex"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="http://www.example.com/genealogy.owl#hasParent"/>
                <owl:maxQualifiedCardinality rdf:datatype="http://www.w3.org/2001/XMLSchema#nonNegativeInteger">2</owl:maxQualifiedCardinality>
                <owl:onClass rdf:resource="http://www.example.com/genealogy.owl#Person"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <owl:disjointWith rdf:resource="http://www.example.com/genealogy.owl#Sex"/>
    </owl:Class>
    


    <!-- http://www.example.com/genealogy.owl#Sex -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Sex">
        <owl:equivalentClass>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="http://www.example.com/genealogy.owl#Female"/>
                    <rdf:Description rdf:about="http://www.example.com/genealogy.owl#Male"/>
                </owl:unionOf>
            </owl:Class>
        </owl:equivalentClass>
        <rdfs:subClassOf rdf:resource="http://www.example.com/genealogy.owl#DomainEntity"/>
    </owl:Class>
    


    <!-- http://www.example.com/genealogy.owl#Woman -->

    <owl:Class rdf:about="http://www.example.com/genealogy.owl#Woman">
        <owl:equivalentClass>
            <owl:Class>
                <owl:intersectionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="http://www.example.com/genealogy.owl#Person"/>
                    <owl:Restriction>
                        <owl:onProperty rdf:resource="http://www.example.com/genealogy.owl#hasSex"/>
                        <owl:someValuesFrom rdf:resource="http://www.example.com/genealogy.owl#Female"/>
                    </owl:Restriction>
                </owl:intersectionOf>
            </owl:Class>
        </owl:equivalentClass>
    </owl:Class>
</rdf:RDF>



<!-- Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi -->


---

# 2. Entries to correct
Below are ONLY the entries that had validation errors. For each one you will see:
- The original input text
- Your previous extraction (triples + entity types)
- The specific SHACL violations found

### entry_1
Text: Origins and Early Ascent
The origins of the House of Habsburg are traced back to the 10th century, specifically to Guntram the Rich, a count in Breisgau. His grandson, Radbot, Count of Klettgau, is credited with building the Habichtsburg (Hawk’s Castle) in the Swiss Canton of Aargau around 1020, from which the family name is derived. Radbot’s marriage to Ida of Lorraine established an early link to the Carolingian bloodline, a crucial bit of "ancestral proof" for their later claims to the Holy Roman Empire.

The transition from local counts to European power players began with Rudolf I of Germany (1218–1291). He was the son of Albert IV, Count of Habsburg, and Hedwig of Kyburg. Upon his election as King of the Romans, Rudolf secured the Duchies of Austria and Styria for his sons, Albert I and Rudolf II, effectively moving the family’s center of power from Switzerland to Vienna. Albert I’s subsequent marriage to Elisabeth of Carinthia produced a staggering fifteen children, ensuring the biological survival of the line but creating a complex web of cadet branches.

The Great Dynastic Split
The most significant expansion occurred under Maximilian I, who used marriage as a tool of statecraft. His own marriage to Mary of Burgundy brought the Low Countries into the Habsburg fold. Their son, Philip the Handsome, married Joanna of Castile (known as Joanna the Mad), the daughter of the "Catholic Monarchs" Ferdinand and Isabella of Spain. This single union merged the Austrian and Spanish legacies.

This resulted in Charles V (Holy Roman Emperor and King of Spain), who arguably held the most complex set of relations in history. Charles V was the grandson of four monarchs: Maximilian I and Mary of Burgundy (paternal), and Ferdinand II of Aragon and Isabella I of Castile (maternal). To manage his vast "Empire on which the sun never sets," Charles eventually abdicated, splitting the house into two distinct but deeply intertwined branches:

The Spanish Habsburgs: Led by his son, Philip II.

The Austrian Habsburgs: Led by his brother, Ferdinand I.

The Inbreeding Spiral
To keep power within the family, the two branches began a centuries-long pattern of intermarriage. Philip II of Spain, for instance, married four times. His second wife, Mary I of England, was his first cousin once removed. His fourth wife, Anna of Austria, was his own niece (the daughter of his sister Mary and his cousin Maximilian II).

This culminated in Charles II of Spain, the "bewitched" king. Genetically, Charles II was more inbred than the offspring of two siblings because his ancestors had married their own nieces and cousins for generations. His father, Philip IV, was the uncle of his mother, Mariana of Austria. Furthermore, Mariana was the daughter of Empress Maria Anna, who was Philip IV’s sister. This means Charles II’s grandmother was also his aunt.
Violations summary:
- Total violations: 10
- Expected correction items: roughly one triple per violation item below (you may satisfy multiple items with one triple only if it is explicitly valid to do so).
Correction items:

Target triple index -1 (no matching existing triple):
- You likely need to ADD new triple(s).

  [1] Correction item
  - focus node: entry_1__Radbot
  - property path: hasFather
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasFather
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasFather> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Man> ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#hasFather> .


  [2] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasFather
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasFather
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasFather> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Man> ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#hasFather> .


  [3] Correction item
  - focus node: entry_1__Radbot
  - property path: hasSex
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasSex
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasSex> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Sex> ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#hasSex> .


  [4] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasSex
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasSex
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasSex> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Sex> ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#hasSex> .


  [5] Correction item
  - focus node: entry_1__Radbot
  - property path: hasMother
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasMother
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasMother> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Woman> ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#hasMother> .


  [6] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasMother
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasMother
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasMother> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Woman> ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#hasMother> .


  [7] Correction item
  - focus node: entry_1__Ida_of_Lorraine
  - property path: hasSex
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Ida_of_Lorraine->fhkb:hasSex
  - source shape:

    <http://www.example.com/genealogy.owl#Woman-hasSex> a sh:PropertyShape ;
    ns1:hasValueWithClass <http://www.example.com/genealogy.owl#Female> ;
    sh:class <http://www.example.com/genealogy.owl#Sex> ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#hasSex> .


  [8] Correction item
  - focus node: entry_1__House_of_Habsburg
  - property path: isAncestorOf
  - value: N/A (missing value violation)
  - constraint: MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__House_of_Habsburg->fhkb:isAncestorOf
  - source shape:

    <http://www.example.com/genealogy.owl#Ancestor-isAncestorOf> a sh:PropertyShape ;
    ns1:hasValueWithClass <http://www.example.com/genealogy.owl#Person> ;
    sh:minCount 1 ;
    sh:path <http://www.example.com/genealogy.owl#isAncestorOf> .


Target triple index 3 (existing triple to edit):
- Current triple: (Radbot, hasRelation, Carolingian_bloodline)
- Current schema types: (Person, DomainEntity)

  [9] Correction item
  - focus node: entry_1__Radbot
  - property path: hasRelation
  - value: entry_1__Carolingian_bloodline
  - constraint: ClassConstraintComponent
  - violation: Value does not have class fhkb:Person
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasRelation> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Person> ;
    sh:path <http://www.example.com/genealogy.owl#hasRelation> .


Target triple index 4 (existing triple to edit):
- Current triple: (Radbot, hasRelation, Habichtsburg)
- Current schema types: (Person, DomainEntity)

  [10] Correction item
  - focus node: entry_1__Radbot
  - property path: hasRelation
  - value: entry_1__Habichtsburg
  - constraint: ClassConstraintComponent
  - violation: Value does not have class fhkb:Person
  - source shape:

    <http://www.example.com/genealogy.owl#Person-hasRelation> a sh:PropertyShape ;
    sh:class <http://www.example.com/genealogy.owl#Person> ;
    sh:path <http://www.example.com/genealogy.owl#hasRelation> .



# 3. Rules (same as before)
- Follow ontological directionality, not linguistic structure.
- Use the most specific relation and entity type available.
- Dates: YYYY_MM_DD. Numbers: plain digits. Labels: underscores for spaces.
- Do NOT include disambiguation brackets in entity names.
- Each triple's subject/object types MUST satisfy the domain/range declared in the ontology.

# 4. Task
Correct ONLY the violated triples for the entries listed above.

Every listed "Correction item" must be addressed. Do not leave any listed violated indexed triple unchanged.

Return JSON in this exact shape:
- top-level key: "entries"
- "entries" must be an OBJECT with keys "entry_1", "entry_2", ... in the same order as listed above

For each `entries.entry_k`:
- "triples": list of corrected factual assertions, each with subject/relation/object entity IDs
- "schemas": list of corrected type-pairs (same length/order as "triples"), where each pair gives ontology class types for that triple's subject and object

Meaning of each part:
- `triples[i]` is the instance-level fact: (`subject`, `relation`, `object`).
- `schemas[i]` is the type signature for `triples[i]`: (`subject` class, `object` class).
- Therefore, each `schemas[i].subject` and `schemas[i].object` MUST be ontology class/type names (e.g., `Person`, `Man`, `Woman`, `Sex`, `DomainEntity`) and NOT entity IDs.

Schema typing constraints:
- Use only class/type identifiers present in the ontology for schema values.
- Never put entry/entity labels in `schemas` (invalid examples: `entry_1__Albert_I`, `Radbot`).
- Keep `triples` and `schemas` aligned one-to-one and in the same order.

Each triple object MUST contain:
- "triple_idx" (integer)
- "subject" (string)
- "relation" (string)
- "object" (string)

Index rules:
- For an existing violated triple, keep its exact `triple_idx` from the prompt.
- Use `triple_idx = -1` ONLY when adding a brand-new triple to satisfy an unmapped violation.
- Do NOT invent arbitrary new positive indices.
- Do NOT return a full re-extraction of the whole text; return only corrections for listed violations.
