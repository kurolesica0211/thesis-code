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
Prince August Wilhelm Heinrich Günther Viktor of Prussia (29 January 1887 – 25 March 1949), nicknamed "Auwi", was the fourth son of German Emperor Wilhelm II by his first wife, Augusta Victoria of Schleswig-Holstein.
Early life

He was born in the Potsdamer Stadtschloss when his grandfather was still the Crown Prince of Prussia.
He spent his youth with his siblings at the New Palace, also in Potsdam, and his school days with his brothers at the Prinzenhaus in Plön in his mother's ancestral Schleswig-Holstein.
Prince August Wilhelm married his cousin Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg on 22 October 1908 at the Berliner Stadtschloss.
The couple had planned to take up residence in Schönhausen Palace in Berlin, but changed their mind when his father, Kaiser Wilhelm, decided to leave his son the Villa Liegnitz in the Sanssouci Park.
In 1912 their only child, Prince Alexander Ferdinand of Prussia, was born.
In the First World War, August Wilhelm was made district administrator (Landrat) of the district of Ruppin; his office and residence was now Schloss Rheinsberg.
His personal adjutant Hans Georg von Mackensen played an important role in his life; the two had been close friends since August Wilhelm's youth.
These "pronounced homophilic tendencies" contributed to the failure of his marriage to Princess Alexandra Victoria.
The couple did not divorce while August Wilhelm's father, Kaiser Wilhelm II, was Emperor, owing to his opposition to the idea.
Weimar Republic

Initially, many Allied and German leaders favored transitioning Germany to a constitutional monarchy with August Wilhelm as either Emperor or regent for one of Crown Prince Wilhelm's children, although this possibility was quickly precluded when Philipp Scheidemann was forced by the pressures of the German Revolution to declare a republic.
August Wilhelm was awarded custody of their son.
After his divorce and the marriage of his friend von Mackensen to Winifred von Neurath, the daughter of Konstantin von Neurath, August Wilhelm lived a reclusive life in his villa in Potsdam.
Involvement with Nazism

August Wilhelm joined the conservative nationalist veterans group Der Stahlhelm (English: "The Steel helmet").
His involvement with the NSDAP and his adoration of Adolf Hitler made August Wilhelm often the subject of mockery by the left-wing press (who gave him the nickname Braunhemdchen Auwi, or "Auwi the Little Brown Shirt"), politicians (French Ambassador André François-Poncet called him Hanswurst "Hans the Brown Sausage") and from the National Socialists themselves (Joseph Goebbels referred to him as a "good-natured but slightly gormless boy").
As a representative of the erstwhile Hohenzollern dynasty, August Wilhelm was deliberately used by the party to gain votes in elections: he was elected as its lead candidate for the Landtag of Prussia in April 1932, and retained his seat until the Landtag's dissolution in October 1933.
Through his appearances at the party's mass rallies, he addressed himself to sections of the population that were lukewarm towards National Socialism and convinced them "that Hitler was not a threat, but a benefactor of the German people and the German Empire".
At the 5 March 1933 election, August Wilhelm was elected as a Nazi deputy to the German Reichstag from electoral constituency 4, Potsdam I, and he would retain this seat until the fall of the Nazi regime.
August Wilhelm held these positions until the fall of the Nazi regime.
However, after the passing of the Enabling Act of 1933 and the establishment of the dictatorship of the Third Reich, the party no longer needed the former prince, who had secretly hoped "that Hitler would one day hoist him or his son Alexander up to the vacant throne of the Kaiser".
One high-profile visit took August Wilhelm to the Passau Hall of the Nibelungs (Nibelungenhalle).
In early February 1945, in the company of the former Crown Princess Cecilie, August Wilhelm fled the approaching Red Army by going from Potsdam to Kronberg to take refuge with his aunt Princess Margaret of Prussia, a sister of his father.
Post-war life

At the end of the Second World War, on 8 May 1945, August Wilhelm was arrested by the U.S. Army and imprisoned in Ludwigsburg.
A young German Jewish refugee started his interrogation as an American soldier.
Immediately after his release, new proceedings were instituted against August Wilhelm.
With his wife, Princess Alexandra of Schleswig-Holstein-Sonderburg-Glücksburg, Prince August Wilhelm had one son:


Regimental commissions until First World War

Chivalric orders

Ancestry

References

External links



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
  AssignClass (532d4692-b4e3-478c-b1b5-4c4a44ed1116)
 Call ID: 532d4692-b4e3-478c-b1b5-4c4a44ed1116
  Args:
    source: August_Wilhelm_of_Prussia
    type: :Man
  AssignClass (b4c57ccd-73fb-4694-ad7c-7835e73e682e)
 Call ID: b4c57ccd-73fb-4694-ad7c-7835e73e682e
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (a5b48cfb-e0c7-44b9-94bc-75e36f212e3c)
 Call ID: a5b48cfb-e0c7-44b9-94bc-75e36f212e3c
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (c5c3d520-72b7-42b8-b460-212fe8cfa1f3)
 Call ID: c5c3d520-72b7-42b8-b460-212fe8cfa1f3
  Args:
    source: Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (282b1866-73b4-4730-96d6-29623b253316)
 Call ID: 282b1866-73b4-4730-96d6-29623b253316
  Args:
    type: :Man
    source: Alexander_Ferdinand_of_Prussia
  AssignClass (e6618c4b-d28a-433e-85a6-ef2ee49a6587)
 Call ID: e6618c4b-d28a-433e-85a6-ef2ee49a6587
  Args:
    source: Margaret_of_Prussia
    type: :Woman
  AddLiteral (75fb27d8-51c5-4d65-bcc0-bfaf1dff389f)
 Call ID: 75fb27d8-51c5-4d65-bcc0-bfaf1dff389f
  Args:
    relation: :hasBirthYear
    literal_value: 1887
    literal_type: xsd:integer
    source: August_Wilhelm_of_Prussia
  AddLiteral (31f858fa-0e90-439d-af15-807349dded8e)
 Call ID: 31f858fa-0e90-439d-af15-807349dded8e
  Args:
    relation: :hasDeathYear
    source: August_Wilhelm_of_Prussia
    literal_type: xsd:integer
    literal_value: 1949
  AddTriple (0e2bf751-ff09-4df6-9f8c-9a6dccc458be)
 Call ID: 0e2bf751-ff09-4df6-9f8c-9a6dccc458be
  Args:
    relation: :hasFather
    target: Wilhelm_II
    source: August_Wilhelm_of_Prussia
  AddTriple (5fcb4e99-cb4f-4a54-a4a1-1729e1f8ab2a)
 Call ID: 5fcb4e99-cb4f-4a54-a4a1-1729e1f8ab2a
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    source: August_Wilhelm_of_Prussia
    relation: :hasMother
  AddTriple (3474fc67-efd2-4a1d-8d01-c99b64826101)
 Call ID: 3474fc67-efd2-4a1d-8d01-c99b64826101
  Args:
    source: Alexander_Ferdinand_of_Prussia
    target: August_Wilhelm_of_Prussia
    relation: :hasFather
  AddTriple (44f16ba7-0f58-4e8a-838c-15dc2df328f3)
 Call ID: 44f16ba7-0f58-4e8a-838c-15dc2df328f3
  Args:
    source: Alexander_Ferdinand_of_Prussia
    target: Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasMother
  AddLiteral (4d76d1d7-1139-4151-86e9-e44d6689431b)
 Call ID: 4d76d1d7-1139-4151-86e9-e44d6689431b
  Args:
    relation: :hasMarriageYear
    source: August_Wilhelm_of_Prussia
    literal_type: xsd:integer
    literal_value: 1908
  AddTriple (ff836e4a-0832-49b4-a663-1effbbf785da)
 Call ID: ff836e4a-0832-49b4-a663-1effbbf785da
  Args:
    relation: :hasRelation
    source: August_Wilhelm_of_Prussia
    target: Margaret_of_Prussia
  AddTriple (43af88d3-e84b-4239-806e-9809c1357e88)
 Call ID: 43af88d3-e84b-4239-806e-9809c1357e88
  Args:
    source: August_Wilhelm_of_Prussia
    target: Wilhelm_II
    relation: :hasParent
  AddTriple (1cfd67c0-5bf4-448a-b1a9-7f4a3fd5d85a)
 Call ID: 1cfd67c0-5bf4-448a-b1a9-7f4a3fd5d85a
  Args:
    target: Margaret_of_Prussia
    source: Wilhelm_II
    relation: :hasSister
  Finish (f62a4692-6a4f-4e17-91d9-63b84733a604)
 Call ID: f62a4692-6a4f-4e17-91d9-63b84733a604
  Args: