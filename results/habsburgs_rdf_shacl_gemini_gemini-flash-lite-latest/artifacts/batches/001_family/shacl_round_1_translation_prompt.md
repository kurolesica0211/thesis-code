# Role
You are a Semantic Web Expert and Data Quality Consultant. Your task is to analyze technical SHACL (Shapes Constraint Language) validation errors and translate them into a clear, actionable correction plan.

# Context
I am constructing a Knowledge Graph based on a provided ontology. Some extracted triples have failed validation. You need to explain these failures simply so they can be corrected in the next step.

# Task
For each violation in the `{violations}` report:
1. **Identify the Subject:** The specific entity (focus node) triggered the error.
2. **Identify the Problem:** The specific property or relation that is missing, extra, or incorrectly formatted.
3. **Explain the Logic:** Why did this fail based on the constraint? (e.g., "This property is not allowed for this class," or "This value must be a URI, but a string was provided").
4. **Define the Fix:** Provide a precise instruction on how to change the triple to satisfy the ontology.

# Ontology
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



# Raw SHACL Violations
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
- Total violations: 13
- Expected correction items: roughly one triple per violation item below (you may satisfy multiple items with one triple only if it is explicitly valid to do so).
Correction items:

Target triple index -1 (no matching existing triple):
- You likely need to ADD new triple(s).

  [1] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasFather
  - ontology definition of the property:

    fhkb:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isFatherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasFather
  - source shape:

    fhkb:Person-hasFather a sh:PropertyShape ;
    sh:class fhkb:Man ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasFather .


  [2] Correction item
  - focus node: entry_1__Ida_of_Lorraine
  - property path: hasFather
  - ontology definition of the property:

    fhkb:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isFatherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Ida_of_Lorraine->fhkb:hasFather
  - source shape:

    fhkb:Person-hasFather a sh:PropertyShape ;
    sh:class fhkb:Man ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasFather .


  [3] Correction item
  - focus node: entry_1__Radbot
  - property path: hasFather
  - ontology definition of the property:

    fhkb:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isFatherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasFather
  - source shape:

    fhkb:Person-hasFather a sh:PropertyShape ;
    sh:class fhkb:Man ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasFather .


  [4] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasSex
  - ontology definition of the property:

    fhkb:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Sex .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasSex
  - source shape:

    fhkb:Person-hasSex a sh:PropertyShape ;
    sh:class fhkb:Sex ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasSex .


  [5] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasMother
  - ontology definition of the property:

    fhkb:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isMotherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Guntram_the_Rich->fhkb:hasMother
  - source shape:

    fhkb:Person-hasMother a sh:PropertyShape ;
    sh:class fhkb:Woman ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasMother .


  [6] Correction item
  - focus node: entry_1__Ida_of_Lorraine
  - property path: hasMother
  - ontology definition of the property:

    fhkb:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isMotherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Ida_of_Lorraine->fhkb:hasMother
  - source shape:

    fhkb:Person-hasMother a sh:PropertyShape ;
    sh:class fhkb:Woman ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasMother .


  [7] Correction item
  - focus node: entry_1__Radbot
  - property path: hasMother
  - ontology definition of the property:

    fhkb:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isMotherOf .

  - value: N/A (missing value violation)
  - constraint: http://www.w3.org/ns/shacl#MinCountConstraintComponent
  - violation: Less than 1 values on ex:entry_1__Radbot->fhkb:hasMother
  - source shape:

    fhkb:Person-hasMother a sh:PropertyShape ;
    sh:class fhkb:Woman ;
    sh:maxCount 1 ;
    sh:minCount 1 ;
    sh:path fhkb:hasMother .


Target triple index 0 (existing triple to edit):
- Current triple: (Guntram_the_Rich, hasAncestor, House_of_Habsburg)
- Current schema types: (Person, DomainEntity)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type DomainEntity:

    fhkb:DomainEntity a owl:Class .


  [8] Correction item
  - focus node: entry_1__Guntram_the_Rich
  - property path: hasAncestor
  - ontology definition of the property:

    fhkb:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:subPropertyOf fhkb:hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf fhkb:isAncestorOf .

  - value: entry_1__House_of_Habsburg
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Guntram_the_Rich is closed. It cannot have value: ex:entry_1__House_of_Habsburg
  - source shape:

    fhkb:Person a rdfs:Class,
        sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Person-hasFather,
        fhkb:Person-hasMother,
        fhkb:Person-hasParent,
        fhkb:Person-hasRelation,
        fhkb:Person-hasSex .


Target triple index 1 (existing triple to edit):
- Current triple: (Radbot, hasAncestor, House_of_Habsburg)
- Current schema types: (Person, DomainEntity)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type DomainEntity:

    fhkb:DomainEntity a owl:Class .


  [9] Correction item
  - focus node: entry_1__Radbot
  - property path: hasAncestor
  - ontology definition of the property:

    fhkb:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:subPropertyOf fhkb:hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf fhkb:isAncestorOf .

  - value: entry_1__House_of_Habsburg
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Radbot is closed. It cannot have value: ex:entry_1__House_of_Habsburg
  - source shape:

    fhkb:Person a rdfs:Class,
        sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Person-hasFather,
        fhkb:Person-hasMother,
        fhkb:Person-hasParent,
        fhkb:Person-hasRelation,
        fhkb:Person-hasSex .


Target triple index 2 (existing triple to edit):
- Current triple: (Radbot, hasPartner, Ida_of_Lorraine)
- Current schema types: (Person, Marriage)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type Marriage:

    fhkb:Marriage a owl:Class ;
    rdfs:subClassOf fhkb:DomainEntity ;
    owl:disjointWith fhkb:Person,
        fhkb:Sex,
        fhkb:Woman .


  [10] Correction item
  - focus node: entry_1__Radbot
  - property path: hasPartner
  - ontology definition of the property:

    fhkb:hasPartner a owl:ObjectProperty ;
    rdfs:domain fhkb:Marriage ;
    rdfs:range fhkb:Person ;
    owl:inverseOf fhkb:isPartnerIn .

  - value: entry_1__Ida_of_Lorraine
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Radbot is closed. It cannot have value: ex:entry_1__Ida_of_Lorraine
  - source shape:

    fhkb:Person a rdfs:Class,
        sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Person-hasFather,
        fhkb:Person-hasMother,
        fhkb:Person-hasParent,
        fhkb:Person-hasRelation,
        fhkb:Person-hasSex .


Target triple index 4 (existing triple to edit):
- Current triple: (Ida_of_Lorraine, hasSex, Female)
- Current schema types: (Person, Sex)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type Sex:

    fhkb:Sex a owl:Class ;
    rdfs:subClassOf fhkb:DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Female fhkb:Male ) ] .


  [11] Correction item
  - focus node: entry_1__Ida_of_Lorraine
  - property path: hasSex
  - ontology definition of the property:

    fhkb:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Sex .

  - value: entry_1__Female
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Ida_of_Lorraine is closed. It cannot have value: ex:entry_1__Female
  - source shape:

    fhkb:Marriage a rdfs:Class,
        sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Marriage-hasFemalePartner,
        fhkb:Marriage-hasMalePartner,
        fhkb:Marriage-hasPartner .


Target triple index 5 (existing triple to edit):
- Current triple: (Radbot, hasRelation, Carolingian_bloodline)
- Current schema types: (Person, DomainEntity)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type DomainEntity:

    fhkb:DomainEntity a owl:Class .


  [12] Correction item
  - focus node: entry_1__Radbot
  - property path: hasRelation
  - ontology definition of the property:

    fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

  - value: entry_1__Carolingian_bloodline
  - constraint: http://www.w3.org/ns/shacl#ClassConstraintComponent
  - violation: Value does not have class fhkb:Person
  - source shape:

    fhkb:Person-hasRelation a sh:PropertyShape ;
    sh:class fhkb:Person ;
    sh:path fhkb:hasRelation .


Target triple index 7 (existing triple to edit):
- Current triple: (Ida_of_Lorraine, hasRelation, Radbot)
- Current schema types: (Person, Person)
- Ontology definitions of the types:
  - Subject type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

  - Object type Person:

    fhkb:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .


  [13] Correction item
  - focus node: entry_1__Ida_of_Lorraine
  - property path: hasRelation
  - ontology definition of the property:

    fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

  - value: entry_1__Radbot
  - constraint: http://www.w3.org/ns/shacl#ClosedConstraintComponent
  - violation: Node ex:entry_1__Ida_of_Lorraine is closed. It cannot have value: ex:entry_1__Radbot
  - source shape:

    fhkb:Marriage a rdfs:Class,
        sh:NodeShape ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property fhkb:Marriage-hasFemalePartner,
        fhkb:Marriage-hasMalePartner,
        fhkb:Marriage-hasPartner .



# Simplified Output Format
| Violation Number | Triple Index | What's Wrong? | How to Fix It |
| :--- | :--- | :--- | :--- |
| [ID] | [Triple Index] | [Simple Logic Explanation] | [Specific Technical Instruction] |

---
**Constraint for LLM:** Focus on the structural and logical requirements of the ontology. Use local names (e.g., `hasFather`) instead of full URIs in the "What's Wrong" column to ensure clarity.