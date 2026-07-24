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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Alexander, Crown Prince of Yugoslavia (Serbian: Александар Карађорђевић, Престолонаследник Југославије, romanized: Aleksandar Karađorđević, Prestolonaslednik Jugoslavije; born 17 July 1945), is the head of the House of Karađorđević, the former royal house of the defunct Kingdom of Yugoslavia and its predecessor the Kingdom of Serbia.
Alexander is the only child of King Peter II and Princess Alexandra of Greece and Denmark.
He held the position of crown prince in the Democratic Federal Yugoslavia for the first four-and-a-half months of his life, until the declaration of the Federal People's Republic of Yugoslavia later in November 1945, when the monarchy was abolished.
In public he claims the crowned royal title of "Alexander II Karadjordjevic" (Serbian: Александар II Карађорђевић, Aleksandar II Karađorđević) as a pretender to the throne.
Through his father, Alexander is a direct descendant of Queen Victoria, through his great-great-grandfather Prince Alfred, Duke of Saxe-Coburg and Gotha, Victoria's second eldest son.
Alexander is known for his support of constitutional monarchism and his humanitarian work.
He left Yugoslavia in April 1941 and arrived in London in June 1941.
Commenting on the event and what happened to his father, Crown Prince Alexander said, "He  was too straight.
On 29 November 1943, AVNOJ (formed by the Partisans) declared themselves the sovereign communist government of Yugoslavia and announced that they would take away all legal rights from the Royal government.
On 10 August 1945, less than a month after Alexander's birth, AVNOJ named the country Democratic Federal Yugoslavia.
On 29 November 1945, the country was declared a communist republic and changed its name to People's Federal Republic of Yugoslavia.
In 1947, all members of Alexander's family except for his granduncle Prince George were deprived of their Yugoslav citizenship and their property was confiscated.
As of 8 July 2015, the High Court in Belgrade found that decree 392, issued by the Presidency of the Presidium of the National Assembly on 3 August 1947, which deprived King Peter II and other members of the House of Karađorđević of their citizenship, was null and void from the moment of its adoption, in the parts pertaining to Crown Prince Alexander, and that all of its legal consequences are thus null and void.
Birth and childhood

Alexander was born in Suite 212 of Claridge's Hotel in Brook Street, Mayfair, London, on 17 July 1945.
The British Government is said to have temporarily ceded sovereignty over the suite in which the birth occurred to Yugoslavia so that the crown prince would be born on Yugoslav territory, though the story may be apocryphal, as there exists no documentary record of this.
Another part of the story says that a box of soil from the homeland was placed under the bed, so the Prince could be born on Yugoslav soil.
It is now Suite 214 and known as the 'Alexander Suite'.
He was the only child of King Peter II and Queen Alexandra of Yugoslavia.
His parents were relatively unable to take care of him due to their various health and financial problems, so Alexander was raised by his maternal grandmother, Princess Aspasia of Greece and Denmark.
Military service

Alexander graduated from the Royal Military Academy Sandhurst in 1966 and was commissioned as an officer into the British Army's 16th/5th The Queen's Royal Lancers regiment, rising to the rank of captain.
After leaving the army in 1972, Alexander, who speaks several languages, pursued a career in international business.
, he married Princess Maria da Gloria of Orléans-Braganza (b. 1946) from the Brazilian imperial family, at the parish church of St. Mary Magdalene.
They are double 4th cousins once removed as both are descendants of Prince Ferdinand of Saxe-Coburg and Gotha (1785–1851) and Princess Maria Antonia von Koháry (1797–1862), as well as of Pedro I, Emperor of Brazil and Archduchess Maria Leopoldina of Austria.
They have three sons: Peter (born 5 February 1980), and fraternal twins: Philip and Alexander (both born 15 January 1982).
Alexander and Maria da Gloria divorced on 19 February 1985.
Maria da Gloria married Ignacio de Medina, Duke of Segorbe (b. 1947), while Crown Prince Alexander married Katherine Clairy Batis, daughter of Robert Batis and Anna Dosti, civilly on 20 September 1985, and religiously the following day, at St. Sava Serbian Orthodox Church, Notting Hill, London.
Since their marriage, she is known as Crown Princess Katherine, as per the royal family's website.
On 16 December 2017, Alexander attended with his wife the state funeral of his first cousin once removed, King Michael of Romania in Bucharest, along with other heads of European royal families and invited guests.
On 19 September 2022, Crown Prince Alexander and his wife Katherine attended the state funeral of his godmother Queen Elizabeth II.
On 6 February 2024, following the news about King Charles' health, Alexander himself revealed that he had been treated for early stage prostate cancer in December 2023.
Return to Yugoslavia

Alexander first came to Yugoslavia in 1991.
He actively worked with the opposition to Slobodan Milošević and moved to Yugoslavia after Milošević had been deposed in 2000.
On 27 February 2001, the parliament of the Federal Republic of Yugoslavia (FRY) passed legislation conferring citizenship on members of the Karađorđević family.
The legislation may also have effectively annulled a decree stripping the family of its citizenship of the Socialist Federal Republic of Yugoslavia (SFRY) in 1947.
Belief in constitutional monarchy

Alexander is a proponent of re-creating a constitutional monarchy in Serbia and sees himself as the rightful king.
He believes that monarchy could give Serbia "stability, continuity and unity".
A number of political parties and organizations support a constitutional parliamentary monarchy in Serbia.
The assassinated former Serbian Prime Minister Zoran Đinđić was often seen in the company of the prince and his family, supporting their campaigns and projects, although his Democratic Party never publicly embraced monarchism.
Crown Prince Alexander has vowed to stay out of politics.
He and Princess Katherine spend considerable time engaging in humanitarian work.
The Crown Prince has, however, increasingly participated in public functions alongside the leaders of Serbia, the former Yugoslav republics and members of the diplomatic corps.
On 11 May 2006, he hosted a reception at the Royal Palace for delegates attending a summit on Serbia and Montenegro.
The reception was attended by the Governor of the National Bank of Serbia, as well as ambassadors and diplomats from Slovenia, Poland, Brazil, Japan, the United States, and Austria.
In addition, we in Serbia and Montenegro must take into account that whatever form we take within the European Union, we have only but one choice and that is to work for the common good of all member nations.
It is also central to take into account that stability in our region will be enhanced when Serbia is fully at peace with itself.
The Crown Prince raised the issue of a royal restoration in the immediate aftermath of the vote.
I strongly believe in a Constitutional Parliamentary Kingdom of Serbia.
Again, we need to be proud, a strong Serbia that is at peace with itself and with its neighbors.
Only if we have a form of governance close to the Serbian soul: the Kingdom of Serbia.
What is most important is the interest of Serbia.
I am ready to meet all our politicians; we have to work together for the common good of Serbia, and to be friends in the name of the future of our country.
I appeal for mature democratic debate in the interest of Serbia.
Serbia must have clear and realistic objectives.
The public also had reservations with Alexander's apparent lack of knowledge of the Serbian language.
On 27 July 2015, newspaper Blic published a poll "Da li Srbija treba da bude monarhija?" ("Should Serbia be a monarchy?"); 49.8% respondents expressed support in a reconstitution of monarchy, 44.6% were opposed and 5.5% were indifferent.
In 2017, an NGO, the Kingdom of Serbia Association, announced that in 2016, they had collected over 123,000 signatures of support for a referendum on Alexander being named king, short of the 150,000 needed to force a constitutional amendment.



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
  AssignClass (737d4053-0a0c-4f29-8832-4682874a6e48)
 Call ID: 737d4053-0a0c-4f29-8832-4682874a6e48
  Args:
    source: :Alexander_Crown_Prince_of_Yugoslavia
    type: :Man
  AssignClass (dc7bb0e7-4252-40fd-b094-240d61fa6027)
 Call ID: dc7bb0e7-4252-40fd-b094-240d61fa6027
  Args:
    type: :Man
    source: :King_Peter_II
  AssignClass (f72a204e-0771-4545-ab6e-15e3766da9ce)
 Call ID: f72a204e-0771-4545-ab6e-15e3766da9ce
  Args:
    source: :Queen_Alexandra_of_Yugoslavia
    type: :Woman
  AssignClass (cdd9716d-f17c-4f47-832f-18e11b76bae1)
 Call ID: cdd9716d-f17c-4f47-832f-18e11b76bae1
  Args:
    type: :Woman
    source: :Princess_Aspasia_of_Greece_and_Denmark
  AssignClass (917532a0-ba1f-4afc-84fa-3698293953ef)
 Call ID: 917532a0-ba1f-4afc-84fa-3698293953ef
  Args:
    type: :Woman
    source: :Princess_Maria_da_Gloria_of_Orleans_Braganza
  AssignClass (62921e84-6718-4ad3-b0e4-1758c61aadee)
 Call ID: 62921e84-6718-4ad3-b0e4-1758c61aadee
  Args:
    source: :Peter
    type: :Man
  AssignClass (96d0faca-55e3-4e44-8d58-2c6be76ab208)
 Call ID: 96d0faca-55e3-4e44-8d58-2c6be76ab208
  Args:
    source: :Philip
    type: :Man
  AssignClass (0f0058e9-285a-4a97-9eda-63db9069f19d)
 Call ID: 0f0058e9-285a-4a97-9eda-63db9069f19d
  Args:
    type: :Man
    source: :Alexander_son
  AssignClass (5fec65f5-732f-4d33-a0d3-1bee31f59811)
 Call ID: 5fec65f5-732f-4d33-a0d3-1bee31f59811
  Args:
    source: :Katherine_Clairy_Batis
    type: :Woman
  AssignClass (6416d04e-6a8a-4dc6-9e98-fe1aa9217839)
 Call ID: 6416d04e-6a8a-4dc6-9e98-fe1aa9217839
  Args:
    type: :Man
    source: :Robert_Batis
  AssignClass (e64e9136-6427-4d59-813c-6d6c4ecd37a0)
 Call ID: e64e9136-6427-4d59-813c-6d6c4ecd37a0
  Args:
    type: :Woman
    source: :Anna_Dosti
  AssignClass (399c9212-4a78-4b72-b079-3b14f18308ad)
 Call ID: 399c9212-4a78-4b72-b079-3b14f18308ad
  Args:
    type: :Man
    source: :Prince_George
  AddLiteral (db354115-43df-4f11-90d9-b7808ad499d4)
 Call ID: db354115-43df-4f11-90d9-b7808ad499d4
  Args:
    relation: :hasBirthYear
    source: :Alexander_Crown_Prince_of_Yugoslavia
    literal_type: xsd:positiveInteger
    literal_value: 1945
  AddTriple (90304834-2822-4eff-b10a-0b8262627c35)
 Call ID: 90304834-2822-4eff-b10a-0b8262627c35
  Args:
    target: :King_Peter_II
    source: :Alexander_Crown_Prince_of_Yugoslavia
    relation: :hasFather
  AddTriple (cbb6578f-36ac-4cee-aa3b-adaf4d5c35a1)
 Call ID: cbb6578f-36ac-4cee-aa3b-adaf4d5c35a1
  Args:
    target: :Queen_Alexandra_of_Yugoslavia
    source: :Alexander_Crown_Prince_of_Yugoslavia
    relation: :hasMother
  AddTriple (6f1e0d95-4da5-4b01-9a8b-b1d120029189)
 Call ID: 6f1e0d95-4da5-4b01-9a8b-b1d120029189
  Args:
    target: :Princess_Aspasia_of_Greece_and_Denmark
    relation: :hasMother
    source: :Queen_Alexandra_of_Yugoslavia
  AddTriple (cd7f069e-80c3-40b5-ac76-3de61a0d3828)
 Call ID: cd7f069e-80c3-40b5-ac76-3de61a0d3828
  Args:
    source: :Alexander_Crown_Prince_of_Yugoslavia
    relation: :hasSon
    target: :Peter
  AddTriple (c48ddf70-f6c4-4411-a504-8739a1f82687)
 Call ID: c48ddf70-f6c4-4411-a504-8739a1f82687
  Args:
    relation: :hasSon
    source: :Alexander_Crown_Prince_of_Yugoslavia
    target: :Philip
  AddTriple (92114e70-43c0-461b-a7e9-f05db0da60fb)
 Call ID: 92114e70-43c0-461b-a7e9-f05db0da60fb
  Args:
    target: :Alexander_son
    relation: :hasSon
    source: :Alexander_Crown_Prince_of_Yugoslavia
  AddTriple (0b56e6f4-6d1c-43a4-becf-5bbdfe0c10d2)
 Call ID: 0b56e6f4-6d1c-43a4-becf-5bbdfe0c10d2
  Args:
    target: :Princess_Maria_da_Gloria_of_Orleans_Braganza
    source: :Peter
    relation: :hasMother
  AddTriple (90c333de-9faf-4f69-905c-c25ba5c48283)
 Call ID: 90c333de-9faf-4f69-905c-c25ba5c48283
  Args:
    source: :Philip
    relation: :hasMother
    target: :Princess_Maria_da_Gloria_of_Orleans_Braganza
  AddTriple (7d3b6640-9dd2-4a01-af67-8096f6c8baee)
 Call ID: 7d3b6640-9dd2-4a01-af67-8096f6c8baee
  Args:
    target: :Princess_Maria_da_Gloria_of_Orleans_Braganza
    source: :Alexander_son
    relation: :hasMother
  AddTriple (9602bbe8-3bc5-4b05-8f00-245977567aca)
 Call ID: 9602bbe8-3bc5-4b05-8f00-245977567aca
  Args:
    target: :Robert_Batis
    source: :Katherine_Clairy_Batis
    relation: :hasFather
  AddTriple (d84d9eab-e896-40f0-834f-8551b9ad014f)
 Call ID: d84d9eab-e896-40f0-834f-8551b9ad014f
  Args:
    source: :Katherine_Clairy_Batis
    relation: :hasMother
    target: :Anna_Dosti
  Finish (55a41bff-1b0f-4321-abd9-8566400865b6)
 Call ID: 55a41bff-1b0f-4321-abd9-8566400865b6
  Args: