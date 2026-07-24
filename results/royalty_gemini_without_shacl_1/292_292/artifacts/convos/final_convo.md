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
  AssignClass (c7a3a89d-d373-495a-8285-d458025bd7c1)
 Call ID: c7a3a89d-d373-495a-8285-d458025bd7c1
  Args:
    source: Princess_Christina_of_the_Netherlands
    type: :Person
  AssignClass (3a83c506-112e-449b-a7f1-4829a75d3b3a)
 Call ID: 3a83c506-112e-449b-a7f1-4829a75d3b3a
  Args:
    type: :Woman
    source: Princess_Christina_of_the_Netherlands
  AddLiteral (69476bd6-b18f-4477-8810-8cdfef72d8c0)
 Call ID: 69476bd6-b18f-4477-8810-8cdfef72d8c0
  Args:
    literal_type: xsd:integer
    source: Princess_Christina_of_the_Netherlands
    relation: :hasBirthYear
    literal_value: 1947
  AddLiteral (6f1510e2-f59e-4025-b085-71fd2346d361)
 Call ID: 6f1510e2-f59e-4025-b085-71fd2346d361
  Args:
    literal_type: xsd:integer
    source: Princess_Christina_of_the_Netherlands
    relation: :hasDeathYear
    literal_value: 2019
  AssignClass (56fb4c4f-926c-4480-b040-1d082f05cb09)
 Call ID: 56fb4c4f-926c-4480-b040-1d082f05cb09
  Args:
    type: :Person
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (9df8a144-ead5-4f08-b073-0410ed6d3f6c)
 Call ID: 9df8a144-ead5-4f08-b073-0410ed6d3f6c
  Args:
    source: Queen_Juliana_of_the_Netherlands
    type: :Woman
  AssignClass (89b0da65-5e56-4159-9b6a-1f64f8038ea2)
 Call ID: 89b0da65-5e56-4159-9b6a-1f64f8038ea2
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (5bf83a35-8d13-4b8b-8aaf-24f4527cd2df)
 Call ID: 5bf83a35-8d13-4b8b-8aaf-24f4527cd2df
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (7b913375-ed56-4c65-ad91-a0594f756d53)
 Call ID: 7b913375-ed56-4c65-ad91-a0594f756d53
  Args:
    relation: :hasMother
    target: Queen_Juliana_of_the_Netherlands
    source: Princess_Christina_of_the_Netherlands
  AddTriple (ab899692-46ca-4dac-9fc6-1e0df95567eb)
 Call ID: ab899692-46ca-4dac-9fc6-1e0df95567eb
  Args:
    target: Prince_Bernhard_of_Lippe-Biesterfeld
    source: Princess_Christina_of_the_Netherlands
    relation: :hasFather
  AssignClass (6c23ab5d-1691-4f2d-af75-975a8245e80a)
 Call ID: 6c23ab5d-1691-4f2d-af75-975a8245e80a
  Args:
    source: Queen_Wilhelmina_of_the_Netherlands
    type: :Person
  AssignClass (0dbb591b-2d53-4e59-b932-385507fef2a2)
 Call ID: 0dbb591b-2d53-4e59-b932-385507fef2a2
  Args:
    source: Queen_Wilhelmina_of_the_Netherlands
    type: :Woman
  AddTriple (d31dd40d-325b-42c4-af88-6ea015453984)
 Call ID: d31dd40d-325b-42c4-af88-6ea015453984
  Args:
    relation: :hasMother
    source: Queen_Juliana_of_the_Netherlands
    target: Queen_Wilhelmina_of_the_Netherlands
  AssignClass (c8ec4a99-6426-4475-bf27-8a80a74050e2)
 Call ID: c8ec4a99-6426-4475-bf27-8a80a74050e2
  Args:
    type: :Person
    source: Princess_Beatrix
  AssignClass (d07f3d1f-ee29-4c61-9dd5-aa16b9b2a6b9)
 Call ID: d07f3d1f-ee29-4c61-9dd5-aa16b9b2a6b9
  Args:
    source: Princess_Beatrix
    type: :Woman
  AssignClass (c180dcf2-6a33-461c-932f-2bd60c54d371)
 Call ID: c180dcf2-6a33-461c-932f-2bd60c54d371
  Args:
    type: :Person
    source: Princess_Irene
  AssignClass (cd25ed39-66cc-4c28-a975-584b01d16945)
 Call ID: cd25ed39-66cc-4c28-a975-584b01d16945
  Args:
    type: :Woman
    source: Princess_Irene
  AssignClass (f9ec1417-ff3a-4d2c-915d-c23700920ea5)
 Call ID: f9ec1417-ff3a-4d2c-915d-c23700920ea5
  Args:
    source: Princess_Margriet
    type: :Person
  AssignClass (f1664dfb-3efa-4f85-8cd6-3feb7634d9bd)
 Call ID: f1664dfb-3efa-4f85-8cd6-3feb7634d9bd
  Args:
    source: Princess_Margriet
    type: :Woman
  AddTriple (eb738956-6b55-4fff-9bcd-a6ab3468e06d)
 Call ID: eb738956-6b55-4fff-9bcd-a6ab3468e06d
  Args:
    relation: :isSisterOf
    source: Princess_Christina_of_the_Netherlands
    target: Princess_Beatrix
  AddTriple (e40a42e7-a9c7-4743-af2e-b6c53f32f8dd)
 Call ID: e40a42e7-a9c7-4743-af2e-b6c53f32f8dd
  Args:
    target: Princess_Irene
    source: Princess_Christina_of_the_Netherlands
    relation: :isSisterOf
  AddTriple (a2929cdb-c1f4-4cd1-a29a-4b795e34aac6)
 Call ID: a2929cdb-c1f4-4cd1-a29a-4b795e34aac6
  Args:
    relation: :isSisterOf
    source: Princess_Christina_of_the_Netherlands
    target: Princess_Margriet
  AssignClass (5ea4392d-761b-4dd5-834e-d92895312d5c)
 Call ID: 5ea4392d-761b-4dd5-834e-d92895312d5c
  Args:
    source: Princess_Armgard_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (c62abd6c-6677-4f48-af7b-5a0d537ba755)
 Call ID: c62abd6c-6677-4f48-af7b-5a0d537ba755
  Args:
    type: :Woman
    source: Princess_Armgard_of_Lippe-Biesterfeld
  AddTriple (0681372c-5208-4328-a5a6-373305c77387)
 Call ID: 0681372c-5208-4328-a5a6-373305c77387
  Args:
    relation: :hasMother
    source: Prince_Bernhard_of_Lippe-Biesterfeld
    target: Princess_Armgard_of_Lippe-Biesterfeld
  AssignClass (765adc19-1e37-4f42-b827-c88dc97ff413)
 Call ID: 765adc19-1e37-4f42-b827-c88dc97ff413
  Args:
    source: Prince_Felix_of_Luxembourg
    type: :Person
  AssignClass (e7fe4feb-1e9b-4a5e-a6dc-16e92e44f75f)
 Call ID: e7fe4feb-1e9b-4a5e-a6dc-16e92e44f75f
  Args:
    source: Prince_Felix_of_Luxembourg
    type: :Man
  AssignClass (d2f92ec4-28d4-46e0-b2e6-5a243ce2017a)
 Call ID: d2f92ec4-28d4-46e0-b2e6-5a243ce2017a
  Args:
    source: Princess_Anne_of_Bourbon-Parma
    type: :Person
  AssignClass (fb2ded80-464f-4b76-93ab-322f42852c39)
 Call ID: fb2ded80-464f-4b76-93ab-322f42852c39
  Args:
    type: :Woman
    source: Princess_Anne_of_Bourbon-Parma
  AssignClass (9780b099-4434-4b3d-b4a5-e1bd8beed5cc)
 Call ID: 9780b099-4434-4b3d-b4a5-e1bd8beed5cc
  Args:
    source: Jorge_Guillermo
    type: :Person
  AssignClass (7d4dfce2-dcfd-4a64-b96b-994c2e32cf48)
 Call ID: 7d4dfce2-dcfd-4a64-b96b-994c2e32cf48
  Args:
    source: Jorge_Guillermo
    type: :Man
  AssignClass (dcc0d510-5f0e-47e6-826f-4991e70ee68e)
 Call ID: dcc0d510-5f0e-47e6-826f-4991e70ee68e
  Args:
    source: Prince_Carlos_Hugo_of_Bourbon-Parma
    type: :Person
  AssignClass (7fa390ce-6f44-4d88-afee-7d4b8bc41d5e)
 Call ID: 7fa390ce-6f44-4d88-afee-7d4b8bc41d5e
  Args:
    type: :Man
    source: Prince_Carlos_Hugo_of_Bourbon-Parma
  AddTriple (e311af4f-f9dc-4cf7-a123-41114200740e)
 Call ID: e311af4f-f9dc-4cf7-a123-41114200740e
  Args:
    target: Princess_Christina_of_the_Netherlands
    source: Princess_Irene
    relation: :isSisterOf
  AddTriple (1f30cacc-a9f9-4514-95c2-b9897da68a40)
 Call ID: 1f30cacc-a9f9-4514-95c2-b9897da68a40
  Args:
    target: Princess_Christina_of_the_Netherlands
    source: Princess_Beatrix
    relation: :isSisterOf
  AddTriple (f629979b-3086-4b15-ad87-ba5c52bcf18f)
 Call ID: f629979b-3086-4b15-ad87-ba5c52bcf18f
  Args:
    relation: :isSisterOf
    source: Princess_Margriet
    target: Princess_Christina_of_the_Netherlands
  AssignClass (d7803da0-542e-409f-89a0-c4c4191220d4)
 Call ID: d7803da0-542e-409f-89a0-c4c4191220d4
  Args:
    type: :Person
    source: Prince_Bernhard_Jr
  AssignClass (dcb4990b-4612-4edb-b581-62315ef6316d)
 Call ID: dcb4990b-4612-4edb-b581-62315ef6316d
  Args:
    source: Prince_Bernhard_Jr
    type: :Man
  AssignClass (44bae798-24e6-46c3-9440-19256c911482)
 Call ID: 44bae798-24e6-46c3-9440-19256c911482
  Args:
    type: :Person
    source: William_II_of_the_Netherlands
  AssignClass (492a81f9-ca22-4c00-9769-141279a23a71)
 Call ID: 492a81f9-ca22-4c00-9769-141279a23a71
  Args:
    type: :Man
    source: William_II_of_the_Netherlands
  Finish (59adc857-a3f2-451f-83af-c959486f2ccd)
 Call ID: 59adc857-a3f2-451f-83af-c959486f2ccd
  Args: