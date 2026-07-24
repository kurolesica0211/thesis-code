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
  AssignClass (7b365271-aef7-4084-a02c-4a4f01ee9efa)
 Call ID: 7b365271-aef7-4084-a02c-4a4f01ee9efa
  Args:
    type: :Woman
    source: :PrincessChristinaOfTheNetherlands
  AssignClass (48184634-24fe-4f47-bb3d-81b4005d3abd)
 Call ID: 48184634-24fe-4f47-bb3d-81b4005d3abd
  Args:
    source: :PrincessChristinaOfTheNetherlands
    type: :Person
  AddLiteral (0d6f0440-9003-46db-b1c4-7cc02a9ea942)
 Call ID: 0d6f0440-9003-46db-b1c4-7cc02a9ea942
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :PrincessChristinaOfTheNetherlands
    literal_value: 1947
  AddLiteral (26d4f9e4-7829-4599-9b0a-6951a036c9df)
 Call ID: 26d4f9e4-7829-4599-9b0a-6951a036c9df
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2019
    source: :PrincessChristinaOfTheNetherlands
  AddLiteral (06fafa5b-7de6-4f7e-839a-8dcd8bcf45d6)
 Call ID: 06fafa5b-7de6-4f7e-839a-8dcd8bcf45d6
  Args:
    literal_type: xsd:string
    relation: :alsoKnownAs
    literal_value: Maria Christina
    source: :PrincessChristinaOfTheNetherlands
  AddLiteral (7b100f12-0fc9-4366-9f81-40080b3b1edf)
 Call ID: 7b100f12-0fc9-4366-9f81-40080b3b1edf
  Args:
    source: :PrincessChristinaOfTheNetherlands
    literal_value: Princess Marijke
    literal_type: xsd:string
    relation: :formerlyKnownAs
  AssignClass (cf9ac75d-e19b-4092-a6ed-bda0499c30de)
 Call ID: cf9ac75d-e19b-4092-a6ed-bda0499c30de
  Args:
    type: :Woman
    source: :QueenJulianaOfTheNetherlands
  AssignClass (14a8d791-0f8c-4378-8bf4-63a9ced90190)
 Call ID: 14a8d791-0f8c-4378-8bf4-63a9ced90190
  Args:
    source: :QueenJulianaOfTheNetherlands
    type: :Person
  AssignClass (3c02c2aa-e978-40a7-8ddd-4c9642ff7c42)
 Call ID: 3c02c2aa-e978-40a7-8ddd-4c9642ff7c42
  Args:
    source: :PrinceBernhardOfLippeBiesterfeld
    type: :Man
  AssignClass (72b1ff14-3574-4fbd-bec8-8c9e7c3d921d)
 Call ID: 72b1ff14-3574-4fbd-bec8-8c9e7c3d921d
  Args:
    source: :PrinceBernhardOfLippeBiesterfeld
    type: :Person
  AddTriple (73baf3c0-463a-4bab-8e6f-6a3ab04bdb0f)
 Call ID: 73baf3c0-463a-4bab-8e6f-6a3ab04bdb0f
  Args:
    target: :QueenJulianaOfTheNetherlands
    relation: :hasMother
    source: :PrincessChristinaOfTheNetherlands
  AddTriple (ab666f9a-798e-41c3-a9bf-70a2dacc4cde)
 Call ID: ab666f9a-798e-41c3-a9bf-70a2dacc4cde
  Args:
    target: :PrinceBernhardOfLippeBiesterfeld
    relation: :hasFather
    source: :PrincessChristinaOfTheNetherlands
  AssignClass (6c12cf75-585e-4e2c-9733-e53f04e1dcf4)
 Call ID: 6c12cf75-585e-4e2c-9733-e53f04e1dcf4
  Args:
    source: :QueenWilhelminaOfTheNetherlands
    type: :Woman
  AssignClass (e0a64373-9741-49dc-9c4e-ae073fc2f5e8)
 Call ID: e0a64373-9741-49dc-9c4e-ae073fc2f5e8
  Args:
    source: :QueenWilhelminaOfTheNetherlands
    type: :Person
  AddTriple (8d6ef0ce-4a00-473c-9ef0-0d136763cb09)
 Call ID: 8d6ef0ce-4a00-473c-9ef0-0d136763cb09
  Args:
    source: :QueenJulianaOfTheNetherlands
    target: :QueenWilhelminaOfTheNetherlands
    relation: :hasMother
  AssignClass (bf64f311-9123-4321-8c6e-bf4d57b658ca)
 Call ID: bf64f311-9123-4321-8c6e-bf4d57b658ca
  Args:
    source: :PrincessBeatrix
    type: :Woman
  AssignClass (8fde4ac4-a45b-4c77-a106-85ed749f55eb)
 Call ID: 8fde4ac4-a45b-4c77-a106-85ed749f55eb
  Args:
    source: :PrincessBeatrix
    type: :Person
  AssignClass (31946f88-8797-43fc-bdcf-78c6ee684f4e)
 Call ID: 31946f88-8797-43fc-bdcf-78c6ee684f4e
  Args:
    type: :Woman
    source: :PrincessIrene
  AssignClass (53739e4f-98f6-4101-bd73-a76e36299bb8)
 Call ID: 53739e4f-98f6-4101-bd73-a76e36299bb8
  Args:
    source: :PrincessIrene
    type: :Person
  AssignClass (d2134593-7049-4d34-a674-0b605582dfe5)
 Call ID: d2134593-7049-4d34-a674-0b605582dfe5
  Args:
    source: :PrincessMargriet
    type: :Woman
  AssignClass (10edf58d-82d2-4b1d-8975-39bd7ba535ed)
 Call ID: 10edf58d-82d2-4b1d-8975-39bd7ba535ed
  Args:
    source: :PrincessMargriet
    type: :Person
  AddTriple (798eecf3-3a2b-4d1d-9fc1-53d4a16d151b)
 Call ID: 798eecf3-3a2b-4d1d-9fc1-53d4a16d151b
  Args:
    relation: :isSisterOf
    target: :PrincessBeatrix
    source: :PrincessChristinaOfTheNetherlands
  AddTriple (aa7c69e4-619b-4e7e-b669-1bf7c8aa52ca)
 Call ID: aa7c69e4-619b-4e7e-b669-1bf7c8aa52ca
  Args:
    relation: :isSisterOf
    target: :PrincessIrene
    source: :PrincessChristinaOfTheNetherlands
  AddTriple (6defdb2b-6d11-4eb6-ab6c-298ec078d3df)
 Call ID: 6defdb2b-6d11-4eb6-ab6c-298ec078d3df
  Args:
    source: :PrincessChristinaOfTheNetherlands
    target: :PrincessMargriet
    relation: :isSisterOf
  AssignClass (dff7fac0-0e30-4c7d-995f-ea719ce361c4)
 Call ID: dff7fac0-0e30-4c7d-995f-ea719ce361c4
  Args:
    type: :Woman
    source: :PrincessArmgardOfLippeBiesterfeld
  AssignClass (16558035-adc4-4ee2-8aab-f4542fc9acaa)
 Call ID: 16558035-adc4-4ee2-8aab-f4542fc9acaa
  Args:
    type: :Person
    source: :PrincessArmgardOfLippeBiesterfeld
  AddTriple (02afcb57-fab1-468b-bf17-eff3b406c458)
 Call ID: 02afcb57-fab1-468b-bf17-eff3b406c458
  Args:
    source: :PrinceBernhardOfLippeBiesterfeld
    relation: :hasMother
    target: :PrincessArmgardOfLippeBiesterfeld
  AssignClass (e8bd5759-47e6-450e-b773-eb9e78c0cc72)
 Call ID: e8bd5759-47e6-450e-b773-eb9e78c0cc72
  Args:
    type: :Man
    source: :JorgeGuillermo
  AssignClass (0025a347-01cb-4265-b0e9-4fc3d51bdc02)
 Call ID: 0025a347-01cb-4265-b0e9-4fc3d51bdc02
  Args:
    source: :JorgeGuillermo
    type: :Person
  AddLiteral (8fb95d77-278d-46ca-b226-708e5b29802d)
 Call ID: 8fb95d77-278d-46ca-b226-708e5b29802d
  Args:
    literal_value: 1975
    source: :PrincessChristinaOfTheNetherlands
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (1f3d6ac6-720f-4a27-9353-0d601c915de3)
 Call ID: 1f3d6ac6-720f-4a27-9353-0d601c915de3
  Args: