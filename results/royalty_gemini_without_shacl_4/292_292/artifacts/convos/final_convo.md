================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess Christina of the Netherlands (Maria Christina; 18 February 1947 – 16 August 2019) was the youngest of four daughters of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
She taught singing in New York and was a long-term supporter of the Youth Music Foundation in the Netherlands.
Christina died of bone cancer in 2019.
Early life

Princess Christina, who was known as Princess Marijke in her youth, was born on 18 February 1947, at Soestdijk Palace, Baarn, the Netherlands.
Her parents were Crown Princess Juliana, the only child of Queen Wilhelmina of the Netherlands, and Prince Bernhard of Lippe-Biesterfeld.
At the time of her birth, she was fifth in the line to the throne after her mother and three older sisters: Princess Beatrix, Princess Irene and Princess Margriet.
She was baptised on 9 October 1947 and her godparents included Queen Wilhelmina (her maternal grandmother), her eldest sister Princess Beatrix, Sir Winston Churchill (for whom her father stood proxy), her paternal grandmother Princess Armgard of Lippe-Biesterfeld, Prince Felix of Luxembourg, and his niece Princess Anne of Bourbon-Parma.
On 4 September 1948, after a reign of nearly 58 years, Christina's grandmother Queen Wilhelmina (68) abdicated the throne and her mother was inaugurated as Queen of the Kingdom of the Netherlands on 6 September 1948.
Childhood and education

While her mother was pregnant with Christina, she contracted either measles or rubella and as a result, Christina was born nearly blind.
In 1963, she stopped using her first name Maria, from then on referring to herself merely as Christina.
Marriage

While living in New York as Christina van Oranje, the Princess started a relationship with Cuban exile Jorge Guillermo.
Although societal attitudes were changing, because Guillermo was a Catholic, it was still possible that a marriage could cause a public scandal in the Netherlands such as the one that occurred in 1964 when Christina's sister Princess Irene married the Catholic Prince Carlos Hugo of Bourbon-Parma.
Accordingly, Princess Christina, at that time ninth in line for the Dutch throne, renounced her and her descendants' rights to the throne before officially announcing her engagement on St. Valentine's Day, 1975.
After their wedding, they lived in New York but later moved to the Netherlands, where they built Villa Eikenhorst  in Wassenaar, near The Hague.
She recorded and released several CDs (classical, Broadway) in 2000 and 2002, and was a long-term supporter of the Youth Music Foundation in the Netherlands.
In 1989, she allowed her name to be used for the Prinses Christina Concours, an annual competition held in the Netherlands to encourage the musical talents of children in the Netherlands.
One of her few public performances was at the marriage of her nephew Prince Bernhard Jr.
She also sang at the funerals of both of her parents Princess Juliana and Prince Bernhard in the New Church (Delft).
Early 2019, Christina made headlines when she decided to sell several works of art.
These works came to her through inheritance from the Dutch royal family: art lover William II of the Netherlands.
Death

In June 2018, it was announced that Princess Christina had been diagnosed with bone cancer.
Titles, styles and honours

Honours

National honours

Foreign honours

Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (27a81056-dbd9-4599-9734-a0e5b8650fb9)
 Call ID: 27a81056-dbd9-4599-9734-a0e5b8650fb9
  Args:
    source: :Christina_of_the_Netherlands
    type: :Woman
  AssignClass (3361f237-4510-4eb7-beae-6964f9b99b84)
 Call ID: 3361f237-4510-4eb7-beae-6964f9b99b84
  Args:
    type: :Person
    source: :Christina_of_the_Netherlands
  AssignClass (10cdafe4-0d2d-405a-83e8-830f91d71295)
 Call ID: 10cdafe4-0d2d-405a-83e8-830f91d71295
  Args:
    source: :Juliana_of_the_Netherlands
    type: :Woman
  AssignClass (ce52d53c-cb3f-48dd-bcc9-72edb475a3ee)
 Call ID: ce52d53c-cb3f-48dd-bcc9-72edb475a3ee
  Args:
    source: :Juliana_of_the_Netherlands
    type: :Ancestor
  AssignClass (2f059569-4eba-42ec-ab20-861fdb6c5c66)
 Call ID: 2f059569-4eba-42ec-ab20-861fdb6c5c66
  Args:
    source: :Juliana_of_the_Netherlands
    type: :Person
  AssignClass (daf559b0-a79b-40c5-940e-051b418c5c58)
 Call ID: daf559b0-a79b-40c5-940e-051b418c5c58
  Args:
    source: :Bernhard_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (e93c962f-489c-4b56-adc8-2bb37e7ce3ce)
 Call ID: e93c962f-489c-4b56-adc8-2bb37e7ce3ce
  Args:
    type: :Ancestor
    source: :Bernhard_of_Lippe-Biesterfeld
  AssignClass (77bb1465-ff2f-40a8-860a-59f2279e882d)
 Call ID: 77bb1465-ff2f-40a8-860a-59f2279e882d
  Args:
    source: :Bernhard_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (d0d50bb6-ffcc-43d1-b887-2a190e432a29)
 Call ID: d0d50bb6-ffcc-43d1-b887-2a190e432a29
  Args:
    type: :Woman
    source: :Wilhelmina_of_the_Netherlands
  AssignClass (8d73903b-7502-446c-a8d8-4f74edcfce2f)
 Call ID: 8d73903b-7502-446c-a8d8-4f74edcfce2f
  Args:
    source: :Wilhelmina_of_the_Netherlands
    type: :Ancestor
  AssignClass (190aacc5-c653-4c38-89f5-53021eca2ab5)
 Call ID: 190aacc5-c653-4c38-89f5-53021eca2ab5
  Args:
    type: :Person
    source: :Wilhelmina_of_the_Netherlands
  AssignClass (2aeeb846-b459-4d0f-b01d-c4c392e42000)
 Call ID: 2aeeb846-b459-4d0f-b01d-c4c392e42000
  Args:
    type: :Woman
    source: :Beatrix_of_the_Netherlands
  AssignClass (6dd8c299-62d4-4a14-b252-df5562a6030f)
 Call ID: 6dd8c299-62d4-4a14-b252-df5562a6030f
  Args:
    type: :Person
    source: :Beatrix_of_the_Netherlands
  AssignClass (b455cb4b-e68f-495e-98fa-f1c4fd363395)
 Call ID: b455cb4b-e68f-495e-98fa-f1c4fd363395
  Args:
    type: :Woman
    source: :Irene_of_the_Netherlands
  AssignClass (8b7cc5a9-73cd-4c5c-a713-bc8fa57675c9)
 Call ID: 8b7cc5a9-73cd-4c5c-a713-bc8fa57675c9
  Args:
    source: :Irene_of_the_Netherlands
    type: :Person
  AssignClass (c9b69de0-e1d0-4328-8597-0e83f7b0b31b)
 Call ID: c9b69de0-e1d0-4328-8597-0e83f7b0b31b
  Args:
    type: :Woman
    source: :Margriet_of_the_Netherlands
  AssignClass (ecc81b28-9216-4339-9949-fb6e44726656)
 Call ID: ecc81b28-9216-4339-9949-fb6e44726656
  Args:
    source: :Margriet_of_the_Netherlands
    type: :Person
  AddLiteral (1e456298-5986-4b83-848a-c4fd8fe451b4)
 Call ID: 1e456298-5986-4b83-848a-c4fd8fe451b4
  Args:
    source: :Christina_of_the_Netherlands
    literal_value: 1947
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (bb891cfd-9153-4b9f-816d-d2c2957e337f)
 Call ID: bb891cfd-9153-4b9f-816d-d2c2957e337f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2019
    source: :Christina_of_the_Netherlands
  AddTriple (c9378629-df31-4510-a5ca-1780cae429dc)
 Call ID: c9378629-df31-4510-a5ca-1780cae429dc
  Args:
    target: :Bernhard_of_Lippe-Biesterfeld
    relation: :hasFather
    source: :Christina_of_the_Netherlands
  AddTriple (13141ed0-c86a-40cc-8c41-239d8979ad25)
 Call ID: 13141ed0-c86a-40cc-8c41-239d8979ad25
  Args:
    source: :Christina_of_the_Netherlands
    relation: :hasMother
    target: :Juliana_of_the_Netherlands
  AddTriple (ec6431b2-34e5-46f0-8a07-7877f435d31c)
 Call ID: ec6431b2-34e5-46f0-8a07-7877f435d31c
  Args:
    source: :Juliana_of_the_Netherlands
    relation: :hasMother
    target: :Wilhelmina_of_the_Netherlands
  AddTriple (f7e27448-f6e2-4fb6-a487-0d619e1bc492)
 Call ID: f7e27448-f6e2-4fb6-a487-0d619e1bc492
  Args:
    source: :Christina_of_the_Netherlands
    relation: :isSisterOf
    target: :Beatrix_of_the_Netherlands
  AddTriple (8cdaf65c-fdac-402f-832c-a53208b77747)
 Call ID: 8cdaf65c-fdac-402f-832c-a53208b77747
  Args:
    source: :Christina_of_the_Netherlands
    relation: :isSisterOf
    target: :Irene_of_the_Netherlands
  AddTriple (5cf3a342-c571-483a-ac00-5b609a02a03d)
 Call ID: 5cf3a342-c571-483a-ac00-5b609a02a03d
  Args:
    target: :Margriet_of_the_Netherlands
    relation: :isSisterOf
    source: :Christina_of_the_Netherlands
  AddLiteral (3d5f19fb-c460-413d-a55d-2b388ba1147f)
 Call ID: 3d5f19fb-c460-413d-a55d-2b388ba1147f
  Args:
    source: :Christina_of_the_Netherlands
    literal_value: Marijke
    relation: :formerlyKnownAs
    literal_type: xsd:string
  Finish (724ba412-8bc6-4e00-8d93-bfb4940ec4b1)
 Call ID: 724ba412-8bc6-4e00-8d93-bfb4940ec4b1
  Args: