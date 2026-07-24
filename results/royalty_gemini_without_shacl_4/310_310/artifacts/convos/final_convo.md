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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Maurits Willem Pieter Hendrik of Orange-Nassau, van Vollenhoven (born 17 April 1968) is a member of the Dutch royal family as the eldest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Life and career

Maurits was born on 17 April 1968.
His godparents are Princess Christina of the Netherlands, Prince Alois-Konstantin of Lowenstein-Wertheim-Rosenberg, Jhr. G. Krayenhof, and The Dutch Merchant Fleet.
Van Vollenhoven has three brothers: Bernhard, Pieter-Christiaan, Floris.
In 1987, van Vollenhoven performed military service with the Royal Netherlands Marine Corps and the Royal Netherlands Navy.
From September 2001 to May 2006, the prince worked for Philips (Domestic Appliances and Personal Care) in Amersfoort, where he was in charge of part of the Philishave portfolio.
In May 2006, van Vollenhoven started his own business, The Source, which focuses on innovative concepts for products, services and systems for both business and government.
Since 1 May 2013, Maurits is Aide-de-camp to King Willem-Alexander and promoted to the rank of Commander (Dutch: Kapitein-lieutenant ter Zee) in the Royal Netherlands Navy.
Maurits works for Sunrock, a company which invests in solar parks and green energy.
The prince criticised the solar energy policy of the municipality of Amsterdam and opened up about other topics.
Marriage and family

In 1989, van Vollenhoven met Marilène (Marie-Helène) van den Broek b. 4 February 1970, the youngest daughter of Hans van den Broek and Josee van Schendel.
He was the first grandchild of Queen Juliana and Prince Bernhard of the Netherlands who married.
Together, the couple has three children:


By Royal Decree of 26 May 1998, the children of van Vollenhoven bear the surname "van Lippe-Biesterfeld van Vollenhoven", without titles.
Upon the abdication of Queen Beatrix, which took place on 30 April 2013, it was confirmed that the children of Princess Margriet and Pieter van Vollenhoven would no longer be eligible to succeed to the throne, and that they would also cease to be members of the Royal House according to The Membership of the Royal House Act.
Titles and styles

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (b3a0e320-2a10-4ead-9b10-e99fd61c4949)
 Call ID: b3a0e320-2a10-4ead-9b10-e99fd61c4949
  Args:
    type: :Woman
    source: Princess_Beatrix
  AssignClass (f07b4909-477e-4954-8bbf-b69b9c6efd16)
 Call ID: f07b4909-477e-4954-8bbf-b69b9c6efd16
  Args:
    source: Princess_Margriet
    type: :Woman
  AssignClass (ed1a2577-6150-4357-b7b9-d4e9d3c68013)
 Call ID: ed1a2577-6150-4357-b7b9-d4e9d3c68013
  Args:
    source: Pieter_van_Vollenhoven
    type: :Man
  AssignClass (1fc9e573-65ad-40b5-8f54-79009e161b86)
 Call ID: 1fc9e573-65ad-40b5-8f54-79009e161b86
  Args:
    type: :Man
    source: Prince_Maurits
  AddLiteral (f32920cc-8112-49df-91c3-2cdf4a6b7e3e)
 Call ID: f32920cc-8112-49df-91c3-2cdf4a6b7e3e
  Args:
    source: Prince_Maurits
    literal_type: xsd:nonNegativeInteger
    literal_value: 1968
    relation: :hasBirthYear
  AddTriple (e00131ff-c0a4-4fb8-8083-8eb2e39051ab)
 Call ID: e00131ff-c0a4-4fb8-8083-8eb2e39051ab
  Args:
    source: Prince_Maurits
    relation: :hasMother
    target: Princess_Margriet
  AddTriple (e799eb16-d02a-4fa4-9992-65036286e283)
 Call ID: e799eb16-d02a-4fa4-9992-65036286e283
  Args:
    source: Prince_Maurits
    target: Pieter_van_Vollenhoven
    relation: :hasFather
  AssignClass (e2926c33-4080-4904-a4d9-2b37b400b55f)
 Call ID: e2926c33-4080-4904-a4d9-2b37b400b55f
  Args:
    type: :Man
    source: Bernhard_van_Vollenhoven
  AssignClass (f3ba9bee-8cc4-4c7a-8e29-93276c89cbee)
 Call ID: f3ba9bee-8cc4-4c7a-8e29-93276c89cbee
  Args:
    source: Pieter-Christiaan_van_Vollenhoven
    type: :Man
  AssignClass (5e010e47-374e-4413-bae7-d8b71a8f1b68)
 Call ID: 5e010e47-374e-4413-bae7-d8b71a8f1b68
  Args:
    source: Floris_van_Vollenhoven
    type: :Man
  AddTriple (a692f6ea-c342-4fb4-95b8-2227610bc874)
 Call ID: a692f6ea-c342-4fb4-95b8-2227610bc874
  Args:
    target: Prince_Maurits
    relation: :isBrotherOf
    source: Bernhard_van_Vollenhoven
  AddTriple (c112a715-866f-4b98-98dd-1a729091a1b5)
 Call ID: c112a715-866f-4b98-98dd-1a729091a1b5
  Args:
    source: Pieter-Christiaan_van_Vollenhoven
    target: Prince_Maurits
    relation: :isBrotherOf
  AddTriple (40343868-2614-4af0-831b-4273a2550b2d)
 Call ID: 40343868-2614-4af0-831b-4273a2550b2d
  Args:
    source: Floris_van_Vollenhoven
    target: Prince_Maurits
    relation: :isBrotherOf
  AssignClass (daf87cac-371f-4753-b210-21144076b5a5)
 Call ID: daf87cac-371f-4753-b210-21144076b5a5
  Args:
    type: :Woman
    source: Marilène_van_den_Broek
  AddLiteral (b2654869-8b31-4f62-98ca-84b4a8ef04e1)
 Call ID: b2654869-8b31-4f62-98ca-84b4a8ef04e1
  Args:
    relation: :hasBirthYear
    literal_value: 1970
    source: Marilène_van_den_Broek
    literal_type: xsd:nonNegativeInteger
  AddLiteral (561a397c-dc02-49d6-b9f2-38239c33b990)
 Call ID: 561a397c-dc02-49d6-b9f2-38239c33b990
  Args:
    literal_value: 1989
    source: Prince_Maurits
    literal_type: xsd:nonNegativeInteger
    relation: :hasMarriageYear
  AddTriple (3c4fbfd0-a208-4878-ba24-b040546ce9e8)
 Call ID: 3c4fbfd0-a208-4878-ba24-b040546ce9e8
  Args:
    target: Marilène_van_den_Broek
    relation: :hasRelation
    source: Prince_Maurits
  AssignClass (eaf19148-3e2c-4d6d-804e-7cf70c1e3d2a)
 Call ID: eaf19148-3e2c-4d6d-804e-7cf70c1e3d2a
  Args:
    source: Hans_van_den_Broek
    type: :Man
  AssignClass (af7590e6-4665-4a47-8267-7869ad358ef6)
 Call ID: af7590e6-4665-4a47-8267-7869ad358ef6
  Args:
    type: :Woman
    source: Josee_van_Schendel
  AddTriple (e4bbc909-4fed-42da-9a51-4eb9c2330417)
 Call ID: e4bbc909-4fed-42da-9a51-4eb9c2330417
  Args:
    source: Marilène_van_den_Broek
    relation: :hasFather
    target: Hans_van_den_Broek
  AddTriple (8062a2c8-72b2-4e69-bd61-10d08cd0f43c)
 Call ID: 8062a2c8-72b2-4e69-bd61-10d08cd0f43c
  Args:
    target: Josee_van_Schendel
    relation: :hasMother
    source: Marilène_van_den_Broek
  Finish (d089ea4d-5bcf-4e0e-ae5c-84ecb1a93f50)
 Call ID: d089ea4d-5bcf-4e0e-ae5c-84ecb1a93f50
  Args: